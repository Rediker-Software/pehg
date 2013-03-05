from .http import JsonResponse

try:
    import simplejson as json
except ImportError:
    import json


class Api:
    
    def __init__(self, api_name="v1"):
        self.api_name = api_name
        self._resources = {}
    
    def get(self, request):
        resource_data = {}
        
        for resource_name, resource in self._resources.iteritems():
            resource_data[resource_name] = {}
            resource_data[resource_name]["list"] = None
            resource_data[resource_name]["schema"] = None
        
        return JsonResponse(resource_data)
    
    def register_resource(self, resource):
        resource_name = getattr(resource, "resource_name", None)
        
        self._resources[resource_name] = resource
    
    def unregister_resource(self, resource_name):
        if resource_name in self._resources:
            del self._resources[resource_name]
