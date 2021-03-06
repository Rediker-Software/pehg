from django.test import TestCase
from pehg.http import JsonResponse, XmlResponse
from pehg.serializers import JsonSerializer, MultiSerializer, XmlSerializer


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


class TestMultiSerializer(TestCase):
    
    def test_build_content_types(self):
        serializer = MultiSerializer()
        serializer.serializers = [JsonSerializer()]
        serializer._build_content_types()
        
        self.assertEqual(serializer.content_types, JsonSerializer.content_types)
        
        serializer.serializers = [XmlSerializer()]
        serializer._build_content_types()
        self.assertEqual(serializer.content_types, XmlSerializer.content_types)
        
        serializer.serializers = [JsonSerializer(), XmlSerializer()]
        serializer._build_content_types()
        self.assertEqual(serializer.content_types, dict(XmlSerializer.content_types.items() + JsonSerializer.content_types.items()))
    
    def test_serializer_from_content_type(self):
        tests = {
            JsonSerializer: ["json", "application/json"],
            XmlSerializer: ["xml", "application/xml"],
        }
        
        for serializer, content_types in tests.iteritems():
            ms = MultiSerializer([serializer()])
            all_ms = MultiSerializer(tests.keys())
            
            for ct in content_types:
                ser = ms._serializer_from_content_type(ct)
                all_ser = all_ms._serializer_from_content_type(ct)
                
                self.assertTrue(isinstance(ser, serializer))
                self.assertEqual(all_ser, serializer)


class TestXmlSerializer(TestCase):
    
    def setUp(self):
        self.serializer = XmlSerializer()
    
    def test_serialize(self):
        response = self.serializer.serialize({"test": "this"})
        self.assertEqual(response["Content-Type"], "application/xml; charset=utf-8")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, '<?xml version="1.0" encoding="utf-8"?><response><test>this</test></response>')
        self.assertEqual(response.data_dict, {"test": "this"})
        
        response = self.serializer.serialize([{"one": "more"}, {"set": "now"}])
        self.assertEqual(response.content, '<?xml version="1.0" encoding="utf-8"?><response><objects type="list"><object><one>more</one></object><object><set>now</set></object></objects></response>')
        self.assertEqual(response.data_dict, [{"one": "more"}, {"set": "now"}])
