from django.contrib.auth.models import AnonymousUser
from django.http.request import HttpRequest
from django.test import TestCase

from pehg.authentication import DjangoAuthentication, NoAuthentication


class TestDjangoAuthentication(TestCase):
    
    def setUp(self):
        self.auth = DjangoAuthentication()
    
    def test_get_user(self):
        request = HttpRequest()
        request.user = AnonymousUser()
        
        response = self.auth.get_user(request)
        self.assertEqual(response, request.user)
    
    def test_is_authenticated(self):
        request = HttpRequest()
        request.user = AnonymousUser()
        
        response = self.auth.is_authenticated(request)
        self.assertFalse(response)


class TestNoAuthentication(TestCase):
    
    def setUp(self):
        self.auth = NoAuthentication()
    
    def test_get_user(self):
        response = self.auth.get_user(HttpRequest())
        self.assertEqual(response, None)
    
    def test_is_authenticated(self):
        response = self.auth.is_authenticated(HttpRequest())
        self.assertTrue(response)
