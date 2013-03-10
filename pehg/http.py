from django.http import HttpResponse

try:
    import simplejson as json
except ImportError:
    import json


class HttpCreated(HttpResponse):
    status_code = 201
    
    def __init__(self, location, *args, **kwargs):
        super(HttpCreated, self).__init__(*args, **kwargs)
        
        self['Location'] = location


class JsonResponse(HttpResponse):
    
    def __init__(self, data_dict, *args, **kwargs):
        super(JsonResponse, self).__init__(json.dumps(data_dict), mimetype="application/json", *args, **kwargs)
        
        self.data_dict = data_dict


class XmlResponse(HttpResponse):
    
    def __init__(self, data_dict, *args, **kwargs):
        super(XmlResponse, self).__init__(data_dict, mimetype="application/xml", *args, **kwargs)
        
        self.data_dict = data_dict
