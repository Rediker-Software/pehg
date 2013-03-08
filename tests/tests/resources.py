from django.test import TestCase
from pehg.resources import ModelResource, Resource
from ..models import Apple


class PearResource(Resource):
    resource_name = "pear"


class AppleResource(ModelResource):
    resource_name = "apple"
    model = Apple


class TestResources(TestCase):
    
    def test_urls(self):
        resource = PearResource()
        
        self.assertEqual(len(resource.urls), 2)


class TestModelResources(TestCase):
    
    def setUp(self):
        apple = Apple(name="test")
        apple.save()
    
    def test_test(self):
        resource = AppleResource()
