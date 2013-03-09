from django.http import HttpRequest
from django.test import TestCase

from pehg.datasets import DataSet
from pehg.resources import ModelResource, Resource
from ..models import Apple


class PearResource(Resource):
    resource_name = "pear"
    data_set = DataSet([{"id": 1, "name": "test"}, {"id": 2, "name": "other"}])


class AppleResource(ModelResource):
    fields = ["name", ]
    model = Apple
    resource_name = "apple"


class TestResources(TestCase):
    
    def setUp(self):
        from django.core import urlresolvers
        from pehg.api import Api
        
        api = Api()
        api.register_resource(PearResource())
        
        urlresolvers.get_resolver = lambda x: urlresolvers.RegexURLResolver(r'^api/', api.urls)
    
    def test_dispatch_index(self):
        resource = PearResource()
        
        request = HttpRequest()
        
        test_methods = ["GET", "POST"]
        
        for method in test_methods:
            request.method = method
            
            dispatch_response = resource.dispatch_index(request)
            method_response = getattr(resource, "%s_index" % (method.lower(), ))(request)
            
            self.assertEqual(str(dispatch_response), str(method_response))
            self.assertEqual(type(dispatch_response), type(method_response))
    
    def test_dispatch_details(self):
        resource = PearResource()
        
        request = HttpRequest()
        
        test_methods = ["GET"]#, "POST", "PUT", "DELETE"]
        test_pks_instance = ["1", "2"]
        test_pks_set = ["1;2", "1,2"]
        
        for method in test_methods:
            request.method = method
            
            for pk in test_pks_instance:
                dispatch_response = resource.dispatch_details(request, pk)
                method_response = getattr(resource, "%s_instance" % (method.lower(), ))(request, pk)
                
                self.assertEqual(str(dispatch_response), str(method_response))
                self.assertEqual(type(dispatch_response), type(method_response))
            
            for pks in test_pks_set:
                pass
                #resource.dispatch_details(request, pks)
    
    def test_get_index(self):
        resource = PearResource()
        
        request = HttpRequest()
        request.method = "GET"
        
        response = resource.get_index(request)
        self.assertEqual(len(response.data_dict["pears"]), 2)
    
    def test_urls(self):
        resource = PearResource()
        
        self.assertEqual(len(resource.urls), 3)
    
    def test_validate_request_type(self):
        resource = PearResource()
        
        request = HttpRequest()
        
        test_methods = ["GET", "POST", "PUT", "DELETE"]
        test_dispatch = ["index", "set", "instance"]
        
        for method in test_methods:
            request.method = method
            
            for dispatch in test_dispatch:
                func = resource._validate_request_type(request, dispatch)
                #meth = getattr(resource, "%s_%s" % (method.lower(), dispatch, ))
                
                #self.assertEqual(func, meth)


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
    
    def test_get_instance(self):
        resource = AppleResource()
        
        response = resource.get_instance(self.request, 1)
        self.assertEqual(response.data_dict, {"id": 1, "name": "test"})
