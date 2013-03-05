from django.test import TestCase
from pehg.api import Api

class TestApi(TestCase):
    
    def test_register_resource(self):
        api = Api()
        
        self.assertEqual(len(api._resources), 0)
