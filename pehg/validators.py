class Validator(object):
    
    def is_valid(self, obj):
        serialized = obj.serialize()
        
        obj.unserialize(serialized)
        
        return True
