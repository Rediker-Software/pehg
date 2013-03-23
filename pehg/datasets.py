from django.core.urlresolvers import reverse
import copy


class DataSet:
    
    def __init__(self, data_list, pk="id"):
        self.data = data_list
    
    def count(self):
        return len(self.data)
    
    def create(self, *args, **kwargs):
        pass
    
    def filter(self, *args, **kwargs):
        copied = copy.deepcopy(self)
        
        copied.data = self.data
        
        return copied
    
    def get(self, pk):
        pass
    
    def is_valid(self, obj, validator):
        return validator.is_valid(obj)
    
    def serialize_list(self, fields=[]):
        serialized_data = []
        
        for obj in self.data:
            serialized = self.serialize_obj(obj, fields)
            
            serialized_data.append(serialized)
        
        return serialized_data
    
    def serialize_obj(self, obj, fields=[]):
        if not hasattr(obj, "resource_uri") and hasattr(obj, self._primary_key):
            obj.resource_uri = reverse("%s_details" % (self.resource_name, ), kwargs={"pks": getattr(obj, self._primary_key)})
        return obj.serialize()


class DictionaryDataSet(DataSet):
    
    def __init__(self, dictionary_list, pk="id"):
        from .data_objects import DictionaryDataObject
        
        data_list = []
        
        for dictionary in dictionary_list:
            obj = DictionaryDataObject(dictionary)
            data_list.append(obj)
        
        self.data = data_list
        
        self._primary_key = pk
        self._recreate_dict_by_pk(pk)
    
    def create(self, *args, **kwargs):
        data = self.unserialize_obj(kwargs)
        pk = self.next_pk()
        
        setattr(data, self._primary_key, pk)
        self.data_dict[str(pk)] = data
        self.data.append(data)
        
        return data
    
    def delete(self, pk):
        del self.data_dict[pk]
        
        self.data[:] = [obj for obj in self.data if obj.get(self._primary_key) != pk]
    
    def get(self, pk):
        return self.data_dict[pk]
    
    def next_pk(self):
        highest_int = 0
        
        for obj in self.data:
            if obj.id > highest_int:
                highest_int = obj.id
        
        return highest_int + 1
    
    def unserialize_obj(self, obj):
        from .data_objects import DictionaryDataObject
        
        data = DictionaryDataObject(obj)
        return data
    
    def _recreate_dict_by_pk(self, pk):
        self.data_dict = dict((str(getattr(obj, pk)), obj) for obj in self.data)


class ModelDataSet(DataSet):
    
    def __init__(self, model):
        self.model = model
        self.queryset = model.objects.all()
        self._primary_key = model._meta.pk.name
    
    def count(self):
        return self.queryset.count()
    
    def create(self, *args, **kwargs):
        create = self._obj_create_dict(kwargs)
        m2m = self._obj_m2m_dict(kwargs)
        
        obj = self.unserialize_obj(create)
        obj.save()
        
        for attr, value in m2m.iteritems():
            setattr(obj, attr, value)
        
        if m2m:
            obj.save()
        
        return obj
    
    def delete(self, *args, **kwargs):
        obj = self.get(*args, **kwargs)
        obj.delete()
    
    def filter(self, *args, **kwargs):
        copied = copy.deepcopy(self)
        
        copied.queryset = copied.queryset.filter(*args, **kwargs)
        
        return copied
    
    def get(self, *args, **kwargs):
        return self.queryset.get(*args, **kwargs)
    
    def serialize_list(self, fields=[]):
        if fields:
            fields.append(self._primary_key)
        
        data_list = self.queryset.values(*fields)
        
        for obj in data_list:
            if not "resource_uri" in obj:
                obj["resource_uri"] = reverse("%s_details" % (self.resource_name, ), kwargs={"pks": obj[self._primary_key]})
        
        return list(data_list)
    
    def serialize_obj(self, obj, fields=[]):
        from django.forms.models import model_to_dict
        
        if fields:
            fields.append(self._primary_key)
        
        serialized = model_to_dict(obj, fields)
        
        if not "resource_uri" in serialized:
            serialized["resource_uri"] = reverse("%s_details" % (self.resource_name, ), kwargs={"pks": obj.pk})
            
        return serialized
    
    def unserialize_obj(self, obj):
        obj = self._obj_create_dict(obj)
        
        if "resource_uri" in obj:
            del obj["resource_uri"]
        
        return self.model(**obj)
    
    def _obj_create_dict(self, obj):
        new_obj = {}
        
        for field in self.model._meta.fields:
            internal_type = field.get_internal_type()
            
            if internal_type != "ManyToManyField":
                if field.name in obj:
                    new_obj[field.name] = obj[field.name]
            
        return new_obj
    
    def _obj_m2m_dict(self, obj):
        new_obj = {}
        
        for name, value in obj.iteritems():
            field = self.model._meta.get_field_by_name(name)[0]
            internal_type = field.get_internal_type()
            
            if internal_type == "ManyToManyField":
                new_obj[name] = obj[name]
            
        return new_obj
