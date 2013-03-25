from django.core.urlresolvers import reverse
from django.http import HttpRequest
from django.test import TestCase

from pehg.api import Api
from pehg.resources import Resource


class AppleResource(Resource):
    resource_name = "apple"


class PearResource(Resource):
    resource_name = "pear"


class TestApi(TestCase):
    
    def setUp(self):
        from django.core import urlresolvers
        
        api = Api()
        api.register_resource(AppleResource())
        api.register_resource(PearResource())
        
        urlresolvers.get_resolver = lambda x: urlresolvers.RegexURLResolver(r'^api/', api.urls)
    
    def test_get_index(self):
        api = Api()
        
        response = api.get_index(HttpRequest())
        self.assertEquals(response.content, "{}")
        self.assertEquals(response.status_code, 200)
        
        api.register_resource(AppleResource())
        response = api.get_index(HttpRequest())
        self.assertEqual(response.data_dict, {"apple": {"list": "/v1/apple/", "schema": "/v1/apple/schema/"}})
        
        api.register_resource(PearResource())
        response = api.get_index(HttpRequest())
        self.assertEqual(response.data_dict, {"apple": {"list": "/v1/apple/", "schema": "/v1/apple/schema/"}, "pear": {"list": "/v1/pear/", "schema": "/v1/pear/schema/"}})
    
    def test_register_resource(self):
        api = Api()
        self.assertEqual(len(api._resources), 0)
        
        api.register_resource(AppleResource())
        self.assertEqual(len(api._resources), 1)
        self.assertEqual(api._resources.keys(), ["apple"])
        
        api.register_resource(AppleResource())
        self.assertEqual(len(api._resources), 1)
        self.assertEqual(api._resources.keys(), ["apple"])
        
        api.register_resource(PearResource())
        self.assertEqual(len(api._resources), 2)
        self.assertEqual(sorted(api._resources.keys()), ["apple", "pear"])
    
    def test_unregister_resource(self):
        api = Api()
        api.register_resource(AppleResource())
        api.register_resource(PearResource())
        self.assertEqual(sorted(api._resources.keys()), ["apple", "pear"])
        
        api.unregister_resource("apple")
        self.assertEqual(sorted(api._resources.keys()), ["pear"])
        self.assertEqual(len(api._resources), 1)
        
        api.unregister_resource("pear")
        self.assertEqual(len(api._resources), 0)
        
        api.unregister_resource("invalid")
        self.assertEqual(len(api._resources), 0)
    
    def test_urls(self):
        api = Api()
        
        urls = api.urls
        self.assertEqual(len(urls), 2)
        
        api.register_resource(AppleResource())
        api.register_resource(PearResource())
        urls = api.urls
        self.assertEqual(len(urls), 6)
