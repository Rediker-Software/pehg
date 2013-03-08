import copy


class DataSet:
    
    def __init__(self, data_list):
        self.data = data_list
    
    def count(self):
        return len(self.data)
    
    def filter(self, *args, **kwargs):
        copied = copy.deepcopy(self)
        
        copied.data = self.data
        
        return copied
    
    def serialize_list(self, fields=[]):
        pass
    
    def serialize_obj(self, obj, fields=[]):
        pass


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
    
    def serialize_list(self, fields=[]):
        data_list = self.queryset.values(*fields)
        
        return list(data_list)
    
    def serialize_obj(self, obj, fields=[]):
        from django.forms.models import model_to_dict
        
        return model_to_dict(obj, fields)
