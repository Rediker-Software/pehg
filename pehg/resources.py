try:
    from django.conf.urls import patterns, url
except ImportError:
    from django.conf.urls.defaults import patterns, url


class Resource:
    
    def request_index(self, request):
        pass
    
    @property
    def urls(self):
        patterns_list = [
            url(r"^$", self.request_index, name="%s_index" % (self.resource_name, )),
        ]
        
        url_patterns = patterns("", *patterns_list)
        
        return url_patterns
