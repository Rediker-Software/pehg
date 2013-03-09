class DataObject(object):
    pass

ALLOWED_PROPS = ["internal_dict", ]


class DictionaryDataObject(dict, DataObject):
    def __init__(self, dict):
        self.internal_dict = dict
    
    def __unicode__(self):
        return "<DictionaryDataObject: %s>" % (self.internal_dict, )
    
    def __getattr__(self, key):
        if key in ALLOWED_PROPS:
            return super(DictionaryDataObject, self).__getattr__(key)
        
        if key in self.internal_dict:
            return self.internal_dict[key]
        
        raise AttributeError
    
    def __setattr__(self, key, value):
        if key in ALLOWED_PROPS:
            return super(DictionaryDataObject, self).__setattr__(key, value)
        
        self.internal_dict[key] = value
    
    def __getitem__(self, key):
        return self.__getattr__(key)
    
    def __setitem__(self, key, value):
        return self.__setattr__(key, value)
    
    def serialize(self):
        return self.internal_dict
    
    def unserialize(self, serialized_dict):
        self.internal_dict = serialized_dict
