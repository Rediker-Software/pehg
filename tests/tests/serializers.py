from django.test import TestCase
from pehg.http import JsonResponse
from pehg.serializers import JsonSerializer


class TestJsonSerializer(TestCase):
    
    def setUp(self):
        self.serializer = JsonSerializer()
    
    def test_serialize(self):
        response = self.serializer.serialize({"test": "this"})
        self.assertEqual(response.data_dict, {"test": "this"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, '{"test": "this"}')
        self.assertTrue(isinstance(response, JsonResponse))
    
    def test_unserialize(self):
        result = self.serializer.unserialize('{"test": "this"}')
        self.assertEqual(result, {"test": "this"})
        
        result = self.serializer.unserialize('["one", "two", "three"]')
        self.assertEqual(result, ["one", "two", "three"])
