from django.http import HttpResponse

try:
    import simplejson as json
except ImportError:
    import json


class JsonResponse(HttpResponse):
    
    def __init__(self, data_dict, *args, **kwargs):
        super(JsonResponse, self).__init__(json.dumps(data_dict), mimetype="text/json", *args, **kwargs)
