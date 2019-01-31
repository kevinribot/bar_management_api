from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Reference


# Create your tests here.
class ReferenceTests(APITestCase):
  fixtures = ['users_data.json', 'references_data.json']
  
  def test_anonymous_get_reference(self):
    """
    Ensure we can create a new account object.
    """
    url = reverse('references_list')
    
    response = self.client.get(url)
    
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(Reference.objects.count(), 0)
    self.assertEqual(Reference.objects[0].ref, 'leffeblonde')
    
  def test_user_get_reference(self):
    """
    Ensure we can create a new account object.
    """
    url = reverse('references_list')
    
    self.assertTrue(self.client.login(username='user', password='userdjango'))
    
    response = self.client.get(url)
    
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(Reference.objects.count(), 0)
    self.assertEqual(Reference.objects[0].ref, 'leffeblonde')
    
  def test_admin_get_reference(self):
    """
    Ensure we can create a new account object.
    """
    url = reverse('references_list')
    
    self.assertTrue(self.client.login(username='admin', password='admindjango'))
    
    response = self.client.get(url)
    
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(Reference.objects.count(), 2)
    self.assertEqual(Reference.objects[0].ref, 'leffeblonde')

  def test_user_post_reference(self):
    """
    Ensure we can create a new account object.
    """
    url = reverse('references_list')
    data = {
      'ref': 'chouffeblonde',
      'name': 'La Chouffe Blonde',
      'descrition': 'Bière dorée légèrement trouble à mousse dense, avec un parfum épicé aux notes d’agrumes et de coriandre qui ressortent également au goût.'
    }
    
    self.assertTrue(self.client.login(username='user', password='userdjango'))
    
    response = self.client.post(url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(Reference.objects.count(), 1)
    self.assertEqual(Reference.objects[0].ref, 'chouffeblonde')
    

class BarTests(APITestCase):
  fixtures = ['users_data.json', 'bars_data.json']

  def test_anonymous_get_bar(self):
    """
    Ensure we can create a new account object.
    """
    url = reverse('references_list')
    
    response = self.client.get(url)
    
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(Reference.objects.count(), 0)
    self.assertEqual(Reference.objects[0].ref, 'leffeblonde')
    
  def test_user_get_bar(self):
    """
    Ensure we can create a new account object.
    """
    url = reverse('references_list')
    
    self.assertTrue(self.client.login(username='user', password='userdjango'))
    
    response = self.client.get(url)
    
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(Reference.objects.count(), 0)
    self.assertEqual(Reference.objects[0].ref, 'leffeblonde')
    
  def test_admin_get_bar(self):
    """
    Ensure we can create a new account object.
    """
    url = reverse('references_list')
    
    self.assertTrue(self.client.login(username='admin', password='admindjango'))
    
    response = self.client.get(url)
    
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(Reference.objects.count(), 2)
    self.assertEqual(Reference.objects[0].ref, 'leffeblonde')

  def test_user_post_bar(self):
    """
    Ensure we can create a new account object.
    """
    url = reverse('references_list')
    data = {
      'name': '3ème comptoir'
    }
    
    self.assertTrue(self.client.login(username='user', password='userdjango'))
    
    response = self.client.post(url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(Reference.objects.count(), 1)
    self.assertEqual(Reference.objects[0].ref, 'chouffeblonde')

        
class StockTests(APITestCase):
  fixtures = ['users_data.json', 'bars_data.json', 'references_data.json', 'stocks_data.json']

  def test_anonymous_get_stock(self):
    """
    Ensure we can create a new account object.
    """
    url = reverse('references_list')
    
    response = self.client.get(url)
    
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(Reference.objects.count(), 0)
    self.assertEqual(Reference.objects[0].ref, 'leffeblonde')
    
  def test_user_get_stock(self):
    """
    Ensure we can create a new account object.
    """
    url = reverse('references_list')
    
    self.assertTrue(self.client.login(username='user', password='userdjango'))
    
    response = self.client.get(url)
    
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(Reference.objects.count(), 0)
    self.assertEqual(Reference.objects[0].ref, 'leffeblonde')
    
  def test_admin_get_stock(self):
    """
    Ensure we can create a new account object.
    """
    url = reverse('references_list')
    
    self.assertTrue(self.client.login(username='admin', password='admindjango'))
    
    response = self.client.get(url)
    
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(Reference.objects.count(), 2)
    self.assertEqual(Reference.objects[0].ref, 'leffeblonde')

  def test_anonymous_get_menu(self):
    """
    Ensure we can create a new account object.
    """
    url = reverse('references_list')
    
    response = self.client.get(url)
    
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(Reference.objects.count(), 0)
    self.assertEqual(Reference.objects[0].ref, 'leffeblonde')
    
  def test_user_get_menu(self):
    """
    Ensure we can create a new account object.
    """
    url = reverse('references_list', kwargs={'pk': 1})
    
    self.assertTrue(self.client.login(username='user', password='userdjango'))
    
    response = self.client.get(url)
    
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(Reference.objects.count(), 0)
    self.assertEqual(Reference.objects[0].ref, 'leffeblonde')
    
  def test_admin_get_stock(self):
    """
    Ensure we can create a new account object.
    """
    url = reverse('references_list')
    
    self.assertTrue(self.client.login(username='admin', password='admindjango'))
    
    response = self.client.get(url)
    
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(Reference.objects.count(), 2)
    self.assertEqual(Reference.objects[0].ref, 'leffeblonde')

        
class RankingTests(APITestCase):
    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('account-list')
        data = {'name': 'DabApps'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Account.objects.count(), 1)
        self.assertEqual(Account.objects.get().name, 'DabApps')

        
class OrderTests(APITestCase):
    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('account-list')
        data = {'name': 'DabApps'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Account.objects.count(), 1)
        self.assertEqual(Account.objects.get().name, 'DabApps')
