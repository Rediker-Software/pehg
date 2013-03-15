from django.contrib.auth.models import Permission
from django.http import HttpRequest
from django.test import TestCase
from pehg.authentication import DjangoAuthentication
from pehg.authorization import DjangoAuthorization, NoAuthorization
from pehg.resources import ModelResource
from ..models import Apple


class TestDjangoAuthorization(TestCase):
    
    def setUp(self):
        from django.contrib.auth.models import User
        self.user = User.objects.create_user("test", "test@test.com", "test")
        
        self.auth = DjangoAuthorization()
    
    def test_can_create(self):
        
        class TestResource(ModelResource):
            fields = ["name", ]
            model = Apple
            resource_name = "apple"
            
            authentication = DjangoAuthentication()
            authorization = DjangoAuthorization()
        
        request = HttpRequest()
        request.user = self.user
        
        resource = TestResource()
        
        response = self.auth.can_create(self.user, resource)
        self.assertFalse(response)
        
        permission = Permission.objects.get(codename="add_apple")
        self.user.user_permissions.add(permission)
        self.user.save()
        
        del self.user._perm_cache
        
        response = self.auth.can_create(self.user, resource)
        self.assertTrue(response)
    
    def test_can_view(self):
        response = self.auth.can_view(None, None, None)
        self.assertTrue(response)


class TestNoAuthorization(TestCase):
    
    def setUp(self):
        self.auth = NoAuthorization()
    
    def test_can_create(self):
        response = self.auth.can_create(None, None)
        self.assertTrue(response)
    
    def test_can_delete(self):
        response = self.auth.can_delete(None, None, None)
        self.assertTrue(response)
    
    def test_can_edit(self):
        response = self.auth.can_edit(None, None, None)
        self.assertTrue(response)
    
    def test_can_view(self):
        response = self.auth.can_view(None, None, None)
        self.assertTrue(response)
