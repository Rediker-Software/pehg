class Authorization(object):
    
    def can_create(self, user, resource):
        pass
    
    def can_delete(self, user, resource, data_object):
        pass
    
    def can_edit(self, user, resource, data_object):
        pass
    
    def can_view(self, user, resource, data_object):
        pass


class DjangoAuthorization(Authorization):
    
    def can_create(self, user, resource):
        return user.has_perm(self._build_permission(resource.model, "add"))
    
    def can_delete(self, user, resource, data_object):
        return user.has_perm(self._build_permission(resource.model, "delete"))
    
    def can_edit(self, user, resource, data_object):
        return user.has_perm(self._build_permission(resource.model, "change"))
    
    def can_view(self, user, resource, data_object):
        return True
    
    def _build_permission(self, model, permission_name):
        app_label = model._meta.app_label
        model_name = model._meta.object_name
        
        permission = "%s.%s_%s" % (app_label, permission_name, model_name.lower(), )
        
        return permission


class NoAuthorization(Authorization):
    
    def can_create(self, user, resource):
        return True
    
    def can_delete(self, user, resource, data_object):
        return True
    
    def can_edit(self, user, resource, data_object):
        return True
    
    def can_view(self, user, resource, data_object):
        return True
