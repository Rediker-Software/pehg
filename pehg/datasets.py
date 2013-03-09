import copy


class DataSet:
    
    def __init__(self, data_list, pk="id"):
        self.data = data_list
        self._recreate_dict_by_pk(pk)
    
    def count(self):
        return len(self.data)
    
    def filter(self, *args, **kwargs):
        copied = copy.deepcopy(self)
        
        copied.data = self.data
        
        return copied
    
    def get(self, pk):
        return self.data_dict[pk]
    
    def serialize_list(self, fields=[]):
        return self.data
    
    def serialize_obj(self, obj, fields=[]):
        return obj
    
    def _recreate_dict_by_pk(self, pk):
        self.data_dict = dict((str(obj[pk]), obj) for obj in self.data)


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
