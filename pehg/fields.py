from django.forms import fields


class Field(object):
    form_field = fields.Field()


class CharField(Field):
    form_field = fields.CharField()
