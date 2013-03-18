from django.forms import fields


class Field(object):
    default = None
    nullable = True
    required = False
    
    form_field = fields.Field
    
    def __init__(self, *args, **kwargs):
        allowed_properties = ["default", "nullable", "required", ]
        
        for name, value in kwargs.iteritems():
            if name in allowed_properties:
                current_value = getattr(self, name)
                
                if not value == current_value:
                    setattr(self, name, value)
    
    def serialize(self, value):
        form_field = self.get_form_field()
        
        if hasattr(form_field.widget, "_format_value"):
            value = form_field.widget._format_value(value)
        
        return value
    
    def unserialize(self, value):
        form_field = self.get_form_field()
        
        cleaned = form_field.clean(value)
        
        return cleaned
    
    def generate_schema(self):
        return {
            "default": self.default,
            "nullable": self.nullable,
            "required": self.required,
        }


class CharField(Field):
    
    def get_form_field(self):
        return fields.CharField()


class IntegerField(Field):
    
    default = 0
    
    def __init__(self, min_value=None, max_value=None, *args, **kwargs):
        self.min_value = min_value
        self.max_value = max_value
        
        super(IntegerField, self).__init__(*args, **kwargs)
    
    def get_form_field(self):
        return fields.IntegerField(min_value=self.min_value, max_value=self.max_value)
    
    def generate_schema(self):
        schema = super(IntegerField, self).generate_schema()
        
        schema.update({
            "min_value": self.min_value,
            "max_value": self.max_value,
        })
        
        return schema
