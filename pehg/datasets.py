import copy


class DataSet:
    
    def __init__(self, data_list):
        self.data = data_list


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
