from django.test import TestCase
from pehg.datasets import ModelDataSet
from ..models import Apple


class TestModelDataSet(TestCase):
    
    def setUp(self):
        from django.core import urlresolvers
        from pehg.api import Api
        from .resources import AppleResource
        
        api = Api()
        api.register_resource(AppleResource())
        
        urlresolvers.get_resolver = lambda x: urlresolvers.RegexURLResolver(r'^api/', api.urls)
    
    def test_count(self):
        data = ModelDataSet(Apple)
        
        self.assertEqual(data.count(), 0)
        
        apple = Apple(name="test")
        apple.save()
        self.assertEqual(data.count(), 1)
        
        filtered = data.filter(name="test")
        self.assertEqual(filtered.count(), 1)
        
        empty = data.filter(name="invalid")
        self.assertEqual(empty.count(), 0)
    
    def test_filter(self):
        data = ModelDataSet(Apple)
        apple = Apple(name="test")
        apple.save()
        
        filtered = data.filter(name="test")
        self.assertEqual(len(filtered.queryset), 1)
        self.assertNotEqual(filtered, data)
        
        empty = data.filter(name="invalid")
        self.assertEqual(len(empty.queryset), 0)
        self.assertNotEqual(empty, data)
    
    def test_get(self):
        data = ModelDataSet(Apple)
        apple = Apple(name="test")
        apple.save()
        
        check = data.get(id=1)
        self.assertEqual(apple, check)
    
    def test_serialize_list(self):
        data = ModelDataSet(Apple)
        data.resource_name = "apple"
        
        self.assertEqual(len(data.serialize_list()), 0)
        
        apple = Apple(name="test")
        apple.save()
        self.assertEqual(len(data.serialize_list()), 1)
        self.assertEqual(sorted(data.serialize_list()[0].keys()), ["id", "name", "resource_uri"])
        
        self.assertEqual(len(data.serialize_list(["name"])), 1)
        self.assertEqual(sorted(data.serialize_list(["name"])[0].keys()), ["id", "name", "resource_uri"])
    
    def test_serialize_obj(self):
        data = ModelDataSet(Apple)
        data.resource_name = "apple"
        
        apple = Apple(name="test")
        apple.save()
        
        serialized = data.serialize_obj(apple)
        self.assertEqual(serialized, {"id": 1, "name": "test", "resource_uri": "/v1/apple/1/"})
        
        serialized = data.serialize_obj(apple, ["name"])
        self.assertEqual(serialized, {"id": 1, "name": "test", "resource_uri": "/v1/apple/1/"})
