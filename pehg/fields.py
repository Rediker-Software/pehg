from django.forms import fields


class Field(object):
    form_field = fields.Field
    
    def serialize(self, value):
        form = self.form_field()
        if hasattr(form.widget, "_format_value"):
            value = form.widget._format_value(value)
        
        return value
    
    def unserialize(self, value):
        cleaned = self.form_field().clean(value)
        
        return cleaned


class CharField(Field):
    form_field = fields.CharField
