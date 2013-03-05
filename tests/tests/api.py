from django.test import TestCase
from pehg.api import Api
from pehg.resources import Resource


class AppleResource(Resource):
    resource_name = "apple"


class PearResource(Resource):
    resource_name = "pear"


class TestApi(TestCase):
    
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
