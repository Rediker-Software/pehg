from .http import JsonResponse

try:
    from django.conf.urls import patterns, url
except ImportError:
    from django.conf.urls.defaults import patterns, url


class Resource:
    
    def dispatch_index(self, request):
        pass
    
    def dispatch_details(self, request, pks):
        pass
    
    @property
    def urls(self):
        patterns_list = [
            url(r"^$", self.dispatch_index, name="%s_index" % (self.resource_name, )),
            url(r"^(?P<pks>\w[\w/,;]*)/$", self.dispatch_details, name="%s_details" % (self.resource_name, )),
        ]
        
        url_patterns = patterns("", *patterns_list)
        
        return url_patterns
