class Api:
    
    def __init__(self, api_name="v1"):
        self.api_name = api_name
        self._resources = {}
    
    def register_resource(self, resource):
        resource_name = getattr(resource, "api_name", None)
        
        self._resources[resource_name] = resource
    
    def unregister_resource(self, resource_name):
        del self._resources[resource_name]
    