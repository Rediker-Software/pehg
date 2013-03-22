from django.test import TestCase
from django.forms import fields as django_fields
from pehg import fields


class TestField(TestCase):
    
    def test_init(self):
        field = fields.Field()
        
        self.assertFalse(field.required)
        self.assertTrue(field.nullable)
        self.assertEqual(field.default, None)
        self.assertEqual(field.help_text, None)
        
        field = fields.Field(required=True, nullable=False, default="default", help_text="Custom.")
        
        self.assertTrue(field.required)
        self.assertFalse(field.nullable)
        self.assertEqual(field.default, "default")
        self.assertEqual(field.help_text, "Custom.")
    
    def test_generate_schema(self):
        field = fields.Field()
        schema = field.generate_schema()
        
        self.assertTrue("required" in schema)
        self.assertTrue("nullable" in schema)
        self.assertTrue("help_text" in schema)
        self.assertTrue("default" in schema)
        
        self.assertFalse(schema["required"])
        self.assertTrue(schema["nullable"])
        self.assertEqual(schema["default"], None)
        self.assertEqual(schema["help_text"], None)
        
        field = fields.Field(default="default", help_text="Custom.", nullable=False, required=True)
        schema = field.generate_schema()
        
        self.assertFalse(schema["nullable"])
        self.assertTrue(schema["required"])
        self.assertEqual(schema["default"], "default")
        self.assertEqual(schema["help_text"], "Custom.")
    
    def test_get_form_field(self):
        field = fields.Field()
        
        try:
            form_field = field.get_form_field()
            self.fail("get_form_field is defined in the base Field and does not throw an exception")
        except NotImplementedError:
            pass


class TestCharField(TestCase):
    
    def test_init(self):
        field = fields.CharField()
        
        self.assertEqual(field.help_text, "Unicode string data.")
        self.assertEqual(field.min_length, None)
        self.assertEqual(field.max_length, None)
        
        field = fields.CharField(min_length=1, max_length=999)
        
        self.assertEqual(field.min_length, 1)
        self.assertEqual(field.max_length, 999)
    
    def test_generate_schema(self):
        field = fields.CharField()
        schema = field.generate_schema()
        
        self.assertTrue("min_length" in schema)
        self.assertTrue("max_length" in schema)
        self.assertEqual(schema["min_length"], None)
        self.assertEqual(schema["max_length"], None)
        
        field = fields.CharField(min_length=1, max_length=999)
        schema = field.generate_schema()
        
        self.assertEqual(schema["min_length"], 1)
        self.assertEqual(schema["max_length"], 999)
    
    def test_get_form_field(self):
        field = fields.CharField()
        form_field = field.get_form_field()
        
        self.assertEqual(form_field.min_length, None)
        self.assertEqual(form_field.max_length, None)
        
        field = fields.CharField(min_length=1, max_length=999)
        form_field = field.get_form_field()
        
        self.assertEqual(form_field.min_length, 1)
        self.assertEqual(form_field.max_length, 999)


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
