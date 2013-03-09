from django.views.decorators.csrf import csrf_exempt
from .datasets import ModelDataSet
from .http import JsonResponse
from .validators import Validator

try:
    from django.conf.urls import patterns, url
except ImportError:
    from django.conf.urls.defaults import patterns, url

try:
    import simplejson as json
except ImportError:
    import json


class Resource(object):
    
    allowed_methods = ["GET", "POST", "PUT", "DELETE"]
    
    data_set = None
    
    resource_name = None
    resource_name_plural = None
    
    validator = Validator()
    
    def __init__(self, *args, **kwargs):
        if not self.resource_name_plural:
            self.resource_name_plural = self.resource_name + "s"
        
        if self.data_set:
            self.data_set.resource_name = self.resource_name
        
        if not hasattr(self, "api_fields") and hasattr(self, "fields") and isinstance(self.fields, dict):
            self.api_fields = self._validate_fields(self.fields)
    
    @csrf_exempt
    def dispatch_index(self, request):
        func = self._validate_request_type(request, "index")
        
        return func(request)
    
    @csrf_exempt
    def dispatch_details(self, request, pks):
        import re
        
        pk_list = re.split("[\W;,]", pks)
        
        if len(pk_list) > 1:
            func_type = "set"
        else:
            func_type = "instance"
        
        func = self._validate_request_type(request, func_type)
        
        return func(request, pks)
    
    def get_index(self, request):
        index_data = {}
        index_data[self.resource_name_plural] = self.data_set.serialize_list()
        
        return JsonResponse(index_data)
    
    def get_instance(self, request, pk):
        return JsonResponse(self.data_set.serialize_obj(self.data_set.get(pk=pk)))
    
    def get_set(self, request, pks):
        import re
        
        pk_list = re.split("[\W;,]", pks)
        data_list = []
        
        for pk in pk_list:
            data_list.append(self.data_set.serialize_obj(self.data_set.get(pk=pk)))
        
        return JsonResponse(data_list)
    
    def post_index(self, request):
        from .http import HttpCreated
        
        try:
            request_body = request.body
        except AttributeError:
            request_body = request.raw_post_data
        
        data = json.loads(request_body)
        obj = self.data_set.unserialize_obj(data)
        
        self.data_set.create(**self.data_set.serialize_obj(obj))
        
        return HttpCreated()
    
    def schema(self, request):
        return JsonResponse()
    
    @property
    def urls(self):
        patterns_list = [
            url(r"^$", self.dispatch_index, name="%s_index" % (self.resource_name, )),
            url(r"^schema/$", self.schema, name="%s_schema" % (self.resource_name, )),
            url(r"^(?P<pks>\w[\w/,;]*)/$", self.dispatch_details, name="%s_details" % (self.resource_name, )),
        ]
        
        url_patterns = patterns("", *patterns_list)
        
        return url_patterns
    
    def _validate_fields(self, fields):
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
    
    def _convert_model_to_pehg_fields(self, model):
        from . import fields
        
        api_fields = {}
        
        for field in model._meta.fields:
            if hasattr(self, "fields"):
                if not field.name in self.fields:
                    continue
            
            internal_type = field.get_internal_type()
            
            api_field = fields.Field()
            
            if internal_type in ("CharField", ):
                api_field = fields.CharField()
            
            api_fields[field.name] = api_field
            
        self.api_fields = api_fields
