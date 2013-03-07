from django.test import TestCase
from pehg.resources import Resource


class AppleResource(Resource):
    resource_name = "apple"


class TestResources(TestCase):
    
    def test_urls(self):
        resource = AppleResource()
        
        self.assertEqual(len(resource.urls), 1)
