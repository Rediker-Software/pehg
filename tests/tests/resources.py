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
    
    def test_urls(self):
        resource = PearResource()
        
        self.assertEqual(len(resource.urls), 2)
    
    def test_validate_request_type(self):
        resource = PearResource()
        
        request = HttpRequest()
        request.method = "GET"
        
        func = resource._validate_request_type(request, "index")


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
