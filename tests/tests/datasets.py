from django.test import TestCase
from pehg.datasets import ModelDataSet
from ..models import Apple


class TestModelDataSet(TestCase):
    
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
