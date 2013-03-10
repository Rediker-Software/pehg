from django.test import TestCase
from pehg.http import JsonResponse, XmlResponse
from pehg.serializers import JsonSerializer, XmlSerializer


class TestJsonSerializer(TestCase):
    
    def setUp(self):
        self.serializer = JsonSerializer()
    
    def test_serialize(self):
        response = self.serializer.serialize({"test": "this"})
        self.assertEqual(response.data_dict, {"test": "this"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, '{"test": "this"}')
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertTrue(isinstance(response, JsonResponse))
    
    def test_unserialize(self):
        result = self.serializer.unserialize('{"test": "this"}')
        self.assertEqual(result, {"test": "this"})
        
        result = self.serializer.unserialize('["one", "two", "three"]')
        self.assertEqual(result, ["one", "two", "three"])


class TestXmlSerializer(TestCase):
    
    def setUp(self):
        self.serializer = XmlSerializer()
    
    def test_serialize(self):
        response = self.serializer.serialize({"test": "this"})
        self.assertEqual(response["Content-Type"], "application/xml")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, '<response><test>this</test></response>')
        self.assertEqual(response.data_dict, {"test": "this"})
        
        response = self.serializer.serialize([{"one": "more"}, {"set": "now"}])
        self.assertEqual(response.content, '<response><objects type="list"><object><one>more</one></object><object><set>now</set></object></objects></response>')
        self.assertEqual(response.data_dict, [{"one": "more"}, {"set": "now"}])
