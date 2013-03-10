from django.http import HttpResponse


class HttpCreated(HttpResponse):
    status_code = 201
    
    def __init__(self, location, *args, **kwargs):
        super(HttpCreated, self).__init__(*args, **kwargs)
        
        self['Location'] = location


class JsonResponse(HttpResponse):
    
    def __init__(self, data_dict, *args, **kwargs):
        try:
            import simplejson as json
        except ImportError:
            import json
        
        super(JsonResponse, self).__init__(json.dumps(data_dict), mimetype="application/json", *args, **kwargs)
        
        self.data_dict = data_dict


class XmlResponse(HttpResponse):
    
    def __init__(self, data_dict, *args, **kwargs):
        from .serializers import XmlSerializer
        from xml.etree import ElementTree
        
        serializer = XmlSerializer()
        serialized = serializer._obj_to_xml(data_dict, root=True)
        
        super(XmlResponse, self).__init__(ElementTree.tostring(serialized), mimetype="application/xml", *args, **kwargs)
        
        self.data_dict = data_dict
