from django.http import HttpRequest
from django.test import TestCase

from pehg.resources import ModelResource, Resource
from ..models import Apple


class PearResource(Resource):
    resource_name = "pear"


class AppleResource(ModelResource):
    fields = ["name", ]
    model = Apple
    resource_name = "apple"


class TestResources(TestCase):
    
    def test_dispatch_index(self):
        resource = PearResource()
        
        request = HttpRequest()
        
        test_methods = ["GET"]#, "POST", "PUT", "DELETE"]
        
        for method in test_methods:
            request.method = method
            
            #resource.dispatch_index(request)
    
    def test_dispatch_details(self):
        resource = PearResource()
        
        request = HttpRequest()
        
        test_methods = ["GET"]#, "POST", "PUT", "DELETE"]
        test_pks_instance = ["1", "2"]
        test_pks_set = ["1;2", "1,2"]
        
        for method in test_methods:
            request.method = method
            
            for pks in test_pks_instance:
                pass
                #resource.dispatch_details(request, pks)
            
            for pks in test_pks_set:
                pass
                #resource.dispatch_details(request, pks)
    
    def test_urls(self):
        resource = PearResource()
        
        self.assertEqual(len(resource.urls), 2)
    
    def test_validate_request_type(self):
        resource = PearResource()
        
        request = HttpRequest()
        
        test_methods = ["GET", "POST", "PUT", "DELETE"]
        test_dispatch = ["index", "set", "instance"]
        
        for method in test_methods:
            request.method = method
            
            for dispatch in test_dispatch:
                func = resource._validate_request_type(request, dispatch)


class TestModelResources(TestCase):
    
    def setUp(self):
        apple = Apple(name="test")
        apple.save()
        
        self.request = HttpRequest()
    
    def test_data_set(self):
        resource = AppleResource()
        
        self.assertNotEqual(resource.data_set, None)
    
    def test_get_index(self):
        resource = AppleResource()
        
        response = resource.get_index(self.request)
        self.assertEqual(len(response.data_dict["apples"]), 1)
