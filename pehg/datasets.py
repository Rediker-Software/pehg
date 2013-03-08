class DataSet:
    
    def __init__(self, data_list):
        self.data = data_list


class ModelDataSet(DataSet):
    
    def __init__(self, model):
        self.model = model
