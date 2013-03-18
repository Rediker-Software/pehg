from __future__ import with_statement

from django.http import HttpRequest
from django.test import TestCase

from pehg.datasets import DictionaryDataSet
from pehg.resources import ModelResource, Resource

from ..models import Apple


class PearResource(Resource):
    resource_name = "pear"
    data_set = DictionaryDataSet([{"id": 1, "name": "test"}, {"id": 2, "name": "other"},])


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
        request._read_started = False
        request._body = request._raw_post_data = '{"name": "test"}'
        
        test_methods = ["GET", "POST"]
        
        for method in test_methods:
            request.method = method
            
            dispatch_response = resource.dispatch_index(request)
            method_response = getattr(resource, "%s_index" % (method.lower(), ))(request)
            
            self.assertEqual(dispatch_response.status_code, method_response.status_code)
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
                dispatch_response = resource.dispatch_details(request, pks)
                method_response = getattr(resource, "%s_set" % (method.lower(), ))(request, pks)
                
                self.assertEqual(str(dispatch_response), str(method_response))
                self.assertEqual(type(dispatch_response), type(method_response))
    
    def test_get_index(self):
        resource = PearResource()
        
        request = HttpRequest()
        request.method = "GET"
        
        response = resource.get_index(request)
        
        self.assertEqual(len(response.data_dict["pears"]), len(resource.data_set.data_dict))
    
    def test_not_implemented(self):
        class TestResource(Resource):
            allowed_methods = []
            resource_name = "test"
        
        resource = TestResource()
        
        test_methods = ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"]
        test_types = ["index", "details"]
        
        for method in test_methods:
            self.assertFalse(method in resource.allowed_methods)
            
            request = HttpRequest()
            request.method = method
            
            for type in test_types:
                validate_request_type = resource._validate_request_type(request, type)
                self.assertEqual(validate_request_type, None)
            
            response = resource.dispatch_index(request)
            self.assertEqual(response.status_code, 501)
            
            response = resource.dispatch_details(request, "1")
            self.assertEqual(response.status_code, 501)
    
    def test_urls(self):
        resource = PearResource()
        
        self.assertEqual(len(resource.urls), 5)
    
    def test_validate_request_type(self):
        resource = PearResource()
        
        request = HttpRequest()
        
        test_methods = ["GET"]#, "POST", "PUT", "DELETE"]
        test_dispatch = ["index", "set", "instance"]
        
        for method in test_methods:
            request.method = method
            
            for dispatch in test_dispatch:
                func = resource._validate_request_type(request, dispatch)
                meth = getattr(resource, "%s_%s" % (method.lower(), dispatch, ))
                
                self.assertEqual(func, meth)


class TestModelResources(TestCase):
    
    def setUp(self):
        apple = Apple(name="test")
        apple.save()
        apple2 = Apple(name="other")
        apple2.save()
        
        self.request = HttpRequest()
        self.request._read_started = False
    
    def test_data_set(self):
        resource = AppleResource()
        
        self.assertNotEqual(resource.data_set, None)
    
    def test_get_index(self):
        resource = AppleResource()
        
        with self.assertNumQueries(1):
            response = resource.get_index(self.request)
            self.assertEqual(len(response.data_dict["apples"]), 2)
    
    def test_get_instance(self):
        resource = AppleResource()
        
        with self.assertNumQueries(1):
            response = resource.get_instance(self.request, 1)
            self.assertEqual(response.data_dict, {"id": 1, "name": "test", "resource_uri": "/v1/apple/1/"})
    
    def test_get_set(self):
        resource = AppleResource()
        
        with self.assertNumQueries(1):
            response = resource.get_set(self.request, "1;2")
            self.assertEqual(len(response.data_dict), 2)
    
    def test_post_index(self):
        resource = AppleResource()
        
        with self.assertNumQueries(1):
            self.request._body = self.request._raw_post_data = '{"name": "created"}'
            response = resource.post_index(self.request)
            
            self.assertEqual(response.status_code, 201)
