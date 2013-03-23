from django.views.decorators.csrf import csrf_exempt
from .authentication import NoAuthentication
from .authorization import NoAuthorization
from .datasets import ModelDataSet
from .http import JsonResponse
from .serializers import DEFAULT_SERIALIZERS, MultiSerializer
from .validators import Validator

try:
    from django.conf.urls import patterns, url
except ImportError:
    from django.conf.urls.defaults import patterns, url


class Resource(object):
    
    allowed_methods = ["GET", "POST", "PUT", "DELETE"]
    
    data_set = None
    api_fields = {}
    
    resource_name = None
    resource_name_plural = None
    
    serializer = MultiSerializer(DEFAULT_SERIALIZERS)
    validator = Validator()
    
    authentication = NoAuthentication()
    authorization = NoAuthorization()
    
    _fields = []
    _related_fields = []
    
    def __init__(self, *args, **kwargs):
        if not self.resource_name_plural:
            self.resource_name_plural = self.resource_name + "s"
        
        if self.data_set:
            self.data_set.resource_name = self.resource_name
        
        if not self.api_fields and hasattr(self, "fields") and isinstance(self.fields, dict):
            self.api_fields = self._validate_init_fields(self.fields)
        
        self._fields = []
        self._related_fields = []
        
        for name, field in self.api_fields.iteritems():
            if hasattr(field, "is_relation") and field.is_relation:
                self._related_fields.append(name)
            else:
                self._fields.append(name)
    
    def can_create(self, request):
        user = self.authentication.get_user(request)
        return self.authorization.can_create(user, self)
    
    def can_delete(self, request, data_object):
        user = self.authentication.get_user(request)
        return self.authorization.can_delete(user, self, data_object)
    
    def can_edit(self, request, data_object):
        user = self.authentication.get_user(request)
        return self.authorization.can_edit(user, self, data_object)
    
    def can_view(self, request, data_object):
        user = self.authentication.get_user(request)
        return self.authorization.can_view(user, self, data_object)
    
    @csrf_exempt
    def dispatch_details(self, request, pks, content_type=None):
        from .http import HttpNotImplemented
        import re
        
        if not self.is_authenticated(request):
            raise Exception("You must be authenticated to view this resource")
        
        pk_list = re.split("[\W;,]", pks)
        
        if len(pk_list) > 1:
            func_type = "set"
        else:
            func_type = "instance"
        
        func = self._validate_request_type(request, func_type)
        
        if func is None:
            return HttpNotImplemented()
        
        return func(request, pks, content_type)
    
    @csrf_exempt
    def dispatch_index(self, request, content_type=None):
        from .http import HttpNotImplemented
        
        if not self.is_authenticated(request):
            raise Exception("You must be authenticated to view this resource")
            
        func = self._validate_request_type(request, "index")
        
        if func is None:
            return HttpNotImplemented()
        
        return func(request, content_type)
    
    def get_index(self, request, content_type=None):
        index_data = {}
        index_data[self.resource_name_plural] = self.serialize_list(self._fields)
        
        format = self._determine_content_type_from_request(request, content_type)
        
        return self.serializer.serialize(index_data, format)
    
    def get_instance(self, request, pk, content_type=None):
        format = self._determine_content_type_from_request(request, content_type)
        
        obj = self.data_set.get(pk=pk)
        if not self.can_view(request, obj):
            raise Exception("You do not have permission to view this resource.")
        
        return self.serializer.serialize(self.serialize_obj(obj, self._fields), format)
    
    def get_set(self, request, pks, content_type=None):
        import re
        
        pk_list = re.split("[\W;,]", pks)
        data_list = []
        
        for pk in pk_list:
            obj = self.data_set.get(pk=pk)
            if not self.can_view(request, obj):
                raise Exception("You do not have permission to view this resource.")
                
            data_list.append(self.serialize_obj(obj, self._fields))
        
        format = self._determine_content_type_from_request(request, content_type)
        
        return self.serializer.serialize(data_list, format)
    
    def is_authenticated(self, request):
        return self.authentication.is_authenticated(request)
    
    def post_index(self, request, content_type=None):
        from django.core.exceptions import ValidationError
        from .http import HttpCreated
        
        if not self.can_create(request):
            raise Exception("Not allowed to create on resource")
        
        try:
            request_body = request.body
        except AttributeError:
            request_body = request.raw_post_data
        
        format = self._determine_content_type_from_request(request, content_type)
        data = self.serializer.unserialize(request_body, format)
        
        try:
            obj = self.validate_object(data)
        except ValidationError, e:
            return self.serializer.serialize({"errors": e.messages}, format)
        
        created = self.data_set.create(**obj)
        
        uri = self.serialize_obj(created)["resource_uri"]
        
        return HttpCreated(location=uri)
    
    def schema(self, request, content_type=None):
        if not self.is_authenticated(request):
            raise Exception("You must be authenticated to view this resource")
        
        format = self._determine_content_type_from_request(request, content_type)
        
        response = {
            "allowed_methods": self.allowed_methods,
            "fields": {},
        }
        
        for field_name, field in self.api_fields.iteritems():
            response["fields"][field_name] = field.generate_schema()
        
        return self.serializer.serialize(response, format)
    
    def serialize_list(self, fields=[]):
        obj_list = self.data_set.serialize_list(fields)
        for obj in obj_list:
            for field in self._related_fields:
                obj[field] = self.api_fields[field].serialize(self, obj)
        
        return obj_list
    
    def serialize_obj(self, data, fields=[]):
        obj = self.data_set.serialize_obj(data, fields)
        for field in self._related_fields:
            obj[field] = self.api_fields[field].serialize(self, obj)
            
        return obj
    
    def serialize_set(self, data_set, fields=[]):
        obj_set = data_set.serialize_list(fields)
        for obj in obj_set:
            for field in self._related_fields:
                obj[field] = self.api_fields[field].serialize(self, obj)
        
        return obj_set
    
    @property
    def urls(self):
        patterns_list = [
            url(r"^$", self.dispatch_index, name="%s_index" % (self.resource_name, )),
            url(r"^schema/$", self.schema, name="%s_schema" % (self.resource_name, )),
            url(r"^schema.%s$" % (self._content_types_urlconf()), self.schema, name="%s_schema_ct" % (self.resource_name, )),
            url(r"^(?P<pks>\w[\w/,;]*)/$", self.dispatch_details, name="%s_details" % (self.resource_name, )),
            url(r"^(?P<pks>\w[\w/,;]*).%s$" % (self._content_types_urlconf()), self.dispatch_details, name="%s_details_ct" % (self.resource_name, )),
        ]
        
        url_patterns = patterns("", *patterns_list)
        
        return url_patterns
    
    def validate_object(self, obj):
        from django.core.exceptions import ValidationError
        
        errors = {}
        new_dict = {}
        
        for name, field in self.api_fields.iteritems():
            
            if not name in obj:
                value = None
            else:
                value = obj[name]
            
            try:
                cleaned_value = field.unserialize(value)
                new_dict[name] = cleaned_value
            except ValidationError, e:
                errors[name] = e.messages
        
        if errors:
            error = ValidationError("There were multiple errors when validating the data.")
            error.messages = errors
            
            raise error
        
        return new_dict
    
    def _content_types_urlconf(self):
        types = "|".join(self.serializer.content_types.keys())
        
        return r"(?P<content_type>(%s))" % (types, )
    
    def _determine_content_type_from_request(self, request, content_type=None):
        request_ct = request.META.get("HTTP_ACCEPT", None)
        
        allowed_formats = self.serializer.content_types.keys()
        allowed_cts = self.serializer.content_types.values()
        
        get_format = request.GET.get("format", None)
        
        if get_format and get_format in allowed_formats:
            return self.serializer.content_types[get_format]
        
        if content_type and content_type in allowed_formats:
            return self.serializer.content_types[content_type]
        
        if not request_ct or request_ct == "*/*":
            return "application/json"
        
        ct_list = request_ct.split(";")[0].split(",")
        
        for ct in ct_list:
            if ct in allowed_cts:
                return ct
        
        return "application/json"
        
    def _validate_init_fields(self, fields):
        api_fields = {}
        
        for name, field in fields.iteritems():
            api_fields[name] = field
        
        return api_fields
    
    def _validate_request_type(self, request, dispatch_type):
        request_type = request.method
        request_type = request_type.upper()
        
        dispatch_type = dispatch_type.lower()
        
        if not request_type in self.allowed_methods:
            return
        
        request_type = request_type.lower()
        
        if not hasattr(self, "%s_%s" % (request_type, dispatch_type, )):
            return
        
        func = getattr(self, "%s_%s" % (request_type, dispatch_type, ))
        
        return func


class ModelResource(Resource):
    
    def __init__(self, *args, **kwargs):
        if not self.data_set:
            self.data_set = ModelDataSet(self.model)
        
        self._convert_model_to_pehg_fields(self.model)
        
        super(ModelResource, self).__init__(*args, **kwargs)
    
    def get_set(self, request, pks, content_type=None):
        import re
        
        pk_list = re.split("[\W;,]", pks)
        
        data_list = self.data_set.filter(pk__in=pk_list)
        
        format = self._determine_content_type_from_request(request, content_type)
        
        return self.serializer.serialize(self.serialize_set(data_list, self._fields), format)
    
    def _convert_model_to_pehg_fields(self, model):
        from . import fields
        
        api_fields = {}
        
        for field in model._meta.fields:
            if hasattr(self, "fields"):
                if not field.name in self.fields:
                    continue
            
            internal_type = field.get_internal_type()
            
            api_field = fields.Field()
            
            if internal_type in ("ManyToManyField", "OneToOneField", "ForeignKey", "GenericForeignKey"):
                continue
            
            if internal_type in ("AutoField", ):
                continue
            
            if hasattr(fields, internal_type):
                api_field_class = getattr(fields, internal_type)
                api_field = api_field_class.instance_from_model_field(field)
            
            api_fields[field.name] = api_field
        
        if hasattr(self, "fields") and isinstance(self.fields, dict):
            for name, field in self.fields.iteritems():
                if field:
                    api_fields.update(self._validate_init_fields({name: field}))
            
        self.api_fields = api_fields
