from django.forms import fields, widgets
from django.db.models.fields import NOT_PROVIDED
from django.utils import formats


class Field(object):
    default = None
    help_text = None
    nullable = True
    required = False
    
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


class BooleanField(Field):
    
    default = False
    help_text = "Boolean data."
    
    def get_form_field(self):
        return fields.BooleanField(required=self.required)


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


class DateField(Field):
    
    help_text = "A date as a string."
    
    auto_now = False
    auto_now_add = False
    
    input_formats = formats.get_format('DATE_INPUT_FORMATS')
    
    def __init__(self, auto_now=False, auto_now_add=False, input_formats=None, *args, **kwargs):
        super(DateField, self).__init__(*args, **kwargs)
        
        self.auto_now = auto_now
        self.auto_now_add = auto_now_add
        
        if input_formats:
            self.input_formats = input_formats
    
    def generate_schema(self):
        schema = super(DateField, self).generate_schema()
        
        schema.update({
            "formats": self.input_formats,
        })
        
        return schema
    
    def get_form_field(self):
        return fields.DateField(input_formats=self.input_formats, required=self.required)
    
    @classmethod
    def instance_from_model_field(cls, model):
        field = super(DateField, cls).instance_from_model_field(model)
        
        field.auto_now = model.auto_now
        field.auto_now_add = model.auto_now_add
        
        return field


class DateTimeField(DateField):
    
    help_text = "A date and time as a string."
    input_formats = formats.get_format('DATETIME_INPUT_FORMATS')
    
    def get_form_field(self):
        return fields.DateTimeField(input_formats=self.input_formats, required=self.required)


class DecimalField(Field):
    
    default = 0
    help_text = "Decimal data."
    
    max_digits = None
    decimal_places = None
    
    def __init__(self, max_digits=None, decimal_places=None, *args, **kwargs):
        super(DecimalField, self).__init__(*args, **kwargs)
        
        self.max_digits = max_digits
        self.decimal_places = decimal_places
    
    def generate_schema(self):
        schema = super(DecimalField, self).generate_schema()
        
        schema.update({
            "max_digits": self.max_digits,
            "decimal_places": self.decimal_places,
        })
        
        return schema
    
    def get_form_field(self):
        return fields.DecimalField(max_digits=self.max_digits, decimal_places=self.decimal_places, required=self.required)
    
    @classmethod
    def instance_from_model_field(cls, model):
        instance = super(DecimalField, cls).instance_from_model_field(model)
        
        instance.max_digits = model.max_digits
        instance.decimal_places = model.decimal_places
        
        return instance


class EmailField(CharField):
    
    help_text = "Email address data."
    
    def get_form_field(self):
        return fields.EmailField(min_length=self.min_length, max_length=self.max_length, required=self.required)


class IntegerField(Field):
    
    default = 0
    help_text = "Integer data."
    min_value = None
    max_value = None
    
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


class PositiveIntegerField(IntegerField):
    
    help_text = "Integer data which is positive or zero."
    min_value = 0
    
    def __init__(self, *args, **kwargs):
        return super(PositiveIntegerField, self).__init__(min_value=0, *args, **kwargs)
    
    def get_form_field(self):
        return fields.PositiveIntegerField(max_value=self.max_value, required=self.required)


class TextField(Field):
    
    help_text = "Unicode string data."
    
    def get_form_field(self):
        return fields.CharField(required=self.required)


class TimeField(DateField):
    
    help_text = "A time as a string."
    input_formats = formats.get_format('TIME_INPUT_FORMATS')
    
    def get_form_field(self):
        return fields.TimeField(input_formats=self.input_formats, required=self.required)
