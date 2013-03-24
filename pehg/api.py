from django.core.urlresolvers import reverse
from .http import JsonResponse
from .serializers import DEFAULT_SERIALIZERS, MultiSerializer

try:
    import simplejson as json
except ImportError:
    import json

try:
    from django.conf.urls import include, patterns, url
except ImportError:
    from django.conf.urls.defaults import include, patterns, url


class Api:
    
    serializer = MultiSerializer(DEFAULT_SERIALIZERS)
    
    def __init__(self, api_name="v1"):
        self.api_name = api_name
        self._resources = {}
    
    def get_index(self, request, content_type=None):
        resource_data = {}
        
        for resource_name, resource in self._resources.iteritems():
            resource_data[resource_name] = {}
            resource_data[resource_name]["list"] = reverse("%s_index" % (resource_name, ))
            resource_data[resource_name]["schema"] = reverse("%s_schema" % (resource_name, ))
        
        format = self._determine_content_type_from_request(request, content_type)
        
        return self.serializer.serialize(resource_data, format)
    
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
            url(r"^%s.%s$" % (self.api_name, self._content_types_urlconf(), ), self.get_index, name="api_%s_index_ct" % (self.api_name, )),
        ]
        
        for resource_name, resource in self._resources.iteritems():
            patterns_list += [
                url(r"^%s/%s/" % (self.api_name, resource_name, ), include(resource.urls)),
                url(r"^%s/%s.%s" % (self.api_name, resource_name, resource._content_types_urlconf()), resource.dispatch_index, name="%s_index_ct" % (resource_name, )),
            ]
        
        urlpatterns = patterns("", *patterns_list)
        
        return urlpatterns
    
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
