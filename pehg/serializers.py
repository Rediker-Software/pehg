try:
    import simplejson as json
except ImportError:
    import json


class Serializer(object):
    
    content_types = {}
    
    def serialize(self, obj, format=None):
        pass
    
    def unserialize(self, data, format=None):
        pass


class JsonSerializer(Serializer):
    
    content_types = {"json": "application/json"}
    
    def serialize(self, obj, format="application/json"):
        from .http import JsonResponse
        
        return JsonResponse(obj)
    
    def unserialize(self, data, format="application/json"):
        obj = json.loads(data)
        
        return obj


class MultiSerializer(Serializer):
    
    def __init__(self, serializers=[]):
        self.serializers = serializers
        self._build_content_types()
    
    def serialize(self, obj, format="application/json"):
        if "/" in format:
            serializer = self._serializer_from_content_type(format)
        else:
            if not format in self.content_types:
                return None
            
            format = self.content_types[format]
            
            serializer = self._serializer_from_content_type(format)
        
        return serializer.serialize(obj, format)
    
    def unserialize(self, data, format="application/json"):
        if "/" in format:
            serializer = self._serializer_from_content_type(format)
        else:
            if not format in self.content_types:
                return None
            
            format = self.content_types[format]
            
            serializer = self._serializer_from_content_type(format)
        
        return serializer.unserialize(data, format)
    
    def _build_content_types(self):
        for serializer in self.serializers:
            self.content_types.update(serializer.content_types)
    
    def _serializer_from_content_type(self, content_type):
        reverse_content_types = dict((v,k) for k, v in self.content_types.iteritems())
        
        for serializer in self.serializers:
            if content_type in self.content_types:
                return serializer
                
            if content_type in reverse_content_types:
                return serializer

DEFAULT_SERIALIZERS = [JsonSerializer()]
