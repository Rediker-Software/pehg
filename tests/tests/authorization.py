from django.http import HttpRequest
from django.test import TestCase

from pehg.authorization import NoAuthorization


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
