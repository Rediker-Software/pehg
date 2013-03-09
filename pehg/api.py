from django.core.urlresolvers import reverse
from .http import JsonResponse

try:
    import simplejson as json
except ImportError:
    import json

try:
    from django.conf.urls import include, patterns, url
except ImportError:
    from django.conf.urls.defaults import include, patterns, url


class Api:
    
    def __init__(self, api_name="v1"):
        self.api_name = api_name
        self._resources = {}
    
    def get_index(self, request):
        resource_data = {}
        
        for resource_name, resource in self._resources.iteritems():
            resource_data[resource_name] = {}
            resource_data[resource_name]["list"] = reverse("%s_index" % (resource_name, ))
            resource_data[resource_name]["schema"] = None
        
        return JsonResponse(resource_data)
    
    def register_resource(self, resource):
        resource_name = getattr(resource, "resource_name", None)
        
        self._resources[resource_name] = resource
    
    def unregister_resource(self, resource_name):
        if resource_name in self._resources:
            del self._resources[resource_name]
    
    @property
    def urls(self):
        patterns_list = [
            url(r"^%s/$" % (self.api_name, ), self.get_index, name="api_%s_index" % (self.api_name, )),
        ]
        
        for resource_name, resource in self._resources.iteritems():
            patterns_list += [
                url(r"^%s/%s/" % (self.api_name, resource_name, ), include(resource.urls)),
            ]
        
        urlpatterns = patterns("", *patterns_list)
        
        return urlpatterns
