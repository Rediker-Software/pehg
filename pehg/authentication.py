class Authentication(object):
    
    def is_authenticated(self, request):
        pass


class DjangoAuthentication(Authentication):
    
    def is_authenticated(self, request):
        return request.user.is_active()


class NoAuthentication(Authentication):
    
    def is_authentication(self, request):
        return True
