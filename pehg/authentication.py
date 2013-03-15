class Authentication(object):
    
    def get_user(self, request):
        pass
    
    def is_authenticated(self, request):
        pass


class DjangoAuthentication(Authentication):
    
    def get_user(self, request):
        return request.user
    
    def is_authenticated(self, request):
        return request.user.is_active


class NoAuthentication(Authentication):
    
    def get_user(self, request):
        return None
    
    def is_authenticated(self, request):
        return True
