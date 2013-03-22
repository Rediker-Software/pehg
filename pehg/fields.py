from django.forms import fields
from django.db.models.fields import NOT_PROVIDED


class Field(object):
    default = None
    help_text = None
    nullable = True
    required = False
    
    form_field = fields.Field
    
    def __init__(self, *args, **kwargs):
        allowed_properties = ["default", "help_text", "nullable", "required", ]
        
        for name, value in kwargs.iteritems():
            if name in allowed_properties:
                current_value = getattr(self, name)
                
                if not value == current_value and not value == NOT_PROVIDED:
                    setattr(self, name, value)
    
    @classmethod
    def instance_from_model_field(cls, field):
        default = field.default
        nullable = field.null
        required = False if field.blank else True
        
        return cls(default=default, nullable=nullable, required=required)
    
    def generate_schema(self):
        return {
            "default": self.default,
            "help_text": self.help_text,
            "nullable": self.nullable,
            "required": self.required,
        }
    
    def get_form_field(self):
        raise NotImplementedError("You must define this in your field class.")
    
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
    
    help_text = "Unicode string data."
    
    min_length = None
    max_length = None
    
    def __init__(self, max_length=None, min_length=None, *args, **kwargs):
        super(CharField, self).__init__(*args, **kwargs)
        
        self.min_length = min_length
        self.max_length = max_length
    
    def get_form_field(self):
        return fields.CharField(min_length=self.min_length, max_length=self.max_length, required=self.required)
    
    @classmethod
    def instance_from_model_field(cls, field):
        instance = super(CharField, cls).instance_from_model_field(field)
        
        instance.max_length = field.max_length
        
        return instance
    
    def generate_schema(self):
        schema = super(CharField, self).generate_schema()
        
        schema.update({
            "min_length": self.min_length,
            "max_length": self.max_length,
        })
        
        return schema


class IntegerField(Field):
    
    default = 0
    help_text = "Integer data."
    
    def __init__(self, min_value=None, max_value=None, *args, **kwargs):
        super(IntegerField, self).__init__(*args, **kwargs)
        
        self.min_value = min_value
        self.max_value = max_value
    
    def get_form_field(self):
        return fields.IntegerField(min_value=self.min_value, max_value=self.max_value, required=self.required)
    
    def generate_schema(self):
        schema = super(IntegerField, self).generate_schema()
        
        schema.update({
            "min_value": self.min_value,
            "max_value": self.max_value,
        })
        
        return schema
