from .datasets import ModelDataSet
from .http import JsonResponse

try:
    from django.conf.urls import patterns, url
except ImportError:
    from django.conf.urls.defaults import patterns, url


class Resource(object):
    
    allowed_methods = ["GET", "POST", "PUT", "DELETE"]
    
    data_set = None
    
    resource_name = None
    resource_name_plural = None
    
    def __init__(self, *args, **kwargs):
        if not self.resource_name_plural:
            self.resource_name_plural = self.resource_name + "s"
    
    def dispatch_index(self, request):
        func = self._validate_request_type(request, "index")
        
        return func(request)
    
    def dispatch_details(self, request, pks):
        import re
        
        pk_list = re.split("[\W;,]", pks)
        
        if len(pk_list) > 1:
            func_type = "set"
        else:
            func_type = "instance"
        
        func = self._validate_request_type(request, func_type)
        
        #return func(request)
    
    def get_index(self, request):
        index_data = {}
        index_data[self.resource_name_plural] = self.data_set.serialize_list()
        
        return JsonResponse(index_data)
    
    def post_index(self, request):
        from .http import HttpCreated
        
        return HttpCreated()
    
    @property
    def urls(self):
        patterns_list = [
            url(r"^$", self.dispatch_index, name="%s_index" % (self.resource_name, )),
            url(r"^(?P<pks>\w[\w/,;]*)/$", self.dispatch_details, name="%s_details" % (self.resource_name, )),
        ]
        
        url_patterns = patterns("", *patterns_list)
        
        return url_patterns
    
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
        super(ModelResource, self).__init__(*args, **kwargs)
        
        if not self.data_set:
            self.data_set = ModelDataSet(self.model)
