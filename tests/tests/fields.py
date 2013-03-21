from django.test import TestCase
from django.forms import fields as django_fields
from pehg import fields


class TestIntegerField(TestCase):
    
    def test_init(self):
        field = fields.IntegerField()
        
        self.assertEqual(field.min_value, None)
        self.assertEqual(field.max_value, None)
        self.assertEqual(field.default, 0)
        self.assertEqual(field.help_text, "Integer data.")
        
        field = fields.IntegerField(min_value=1, max_value=999)
        
        self.assertEqual(field.min_value, 1)
        self.assertEqual(field.max_value, 999)
    
    def test_get_form_field(self):
        field = fields.IntegerField()
        form_field = field.get_form_field()
        
        self.assertTrue(isinstance(form_field, django_fields.IntegerField))
        self.assertEqual(form_field.min_value, None)
        self.assertEqual(form_field.max_value, None)
        
        field = fields.IntegerField(min_value=1, max_value=99)
        form_field = field.get_form_field()
        
        self.assertEqual(form_field.min_value, 1)
        self.assertEqual(form_field.max_value, 99)
    
    def test_generate_schema(self):
        field = fields.IntegerField()
        schema = field.generate_schema()
        
        self.assertTrue("min_value" in schema)
        self.assertTrue("max_value" in schema)
        self.assertEqual(schema["min_value"], None)
        self.assertEqual(schema["max_value"], None)
        self.assertEqual(schema["default"], 0)
        
        field = fields.IntegerField(min_value=1, max_value=999)
        schema = field.generate_schema()
        
        self.assertEqual(schema["min_value"], 1)
        self.assertEqual(schema["max_value"], 999)
