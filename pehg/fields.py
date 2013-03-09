from django.forms import fields


class Field(object):
    form_field = fields.Field
    
    def serialize(self, value):
        form_field = self.get_form_field()
        
        if hasattr(form_field.widget, "_format_value"):
            value = form_field.widget._format_value(value)
        
        return value
    
    def unserialize(self, value):
        form_field = self.get_form_field()
        
        cleaned = form_field.clean(value)
        
        return cleaned


class CharField(Field):
    
    def get_form_field(self):
        return fields.CharField()


class IntegerField(Field):
    
    def __init__(self, min_value=None, max_value=None, *args, **kwargs):
        self.min_value = min_value
        self.max_value = max_value
    
    def get_form_field(self):
        return fields.IntegerField(min_value=self.min_value, max_value=self.max_value)
