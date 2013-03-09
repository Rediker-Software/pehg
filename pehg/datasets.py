from django.core.urlresolvers import reverse
import copy


class DataSet:
    
    def __init__(self, data_list, pk="id"):
        self.data = data_list
    
    def count(self):
        return len(self.data)
    
    def filter(self, *args, **kwargs):
        copied = copy.deepcopy(self)
        
        copied.data = self.data
        
        return copied
    
    def get(self, pk):
        pass
    
    def serialize_list(self, fields=[]):
        serialized_data = []
        
        for obj in self.data:
            serialized = self.serialize_obj(obj, fields)
            
            serialized_data.append(serialized)
        
        return serialized_data
    
    def serialize_obj(self, obj, fields=[]):
        if not hasattr(obj, "resource_uri"):
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
    
    def get(self, pk):
        return self.data_dict[pk]
    
    def _recreate_dict_by_pk(self, pk):
        self.data_dict = dict((str(getattr(obj, pk)), obj) for obj in self.data)


class ModelDataSet(DataSet):
    
    def __init__(self, model):
        self.model = model
        self.queryset = model.objects.all()
    
    def count(self):
        return self.queryset.count()
    
    def filter(self, *args, **kwargs):
        copied = copy.deepcopy(self)
        
        copied.queryset = copied.queryset.filter(*args, **kwargs)
        
        return copied
    
    def get(self, *args, **kwargs):
        return self.queryset.get(*args, **kwargs)
    
    def serialize_list(self, fields=[]):
        data_list = self.queryset.values(*fields)
        
        return list(data_list)
    
    def serialize_obj(self, obj, fields=[]):
        from django.forms.models import model_to_dict
        
        return model_to_dict(obj, fields)
