from django.contrib.auth.models import User
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

    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
  def test_user_get_reference(self):
    """
    Ensure we can create a new account object.
    """
    url = reverse('references_list')

    user = User.objects.filter(username='barman').first()
    user.set_password('password1234')
    user.save()

    self.assertTrue(self.client.login(username='barman', password='password1234'))
    
    response = self.client.get('/api/references/')
    references = Reference(response.content.decode("utf-8"))

    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(references[1].ref, 'leffeblonde')
    self.assertEqual(references[1].ref, 'brewdogipa')
    self.assertEqual(references[2].ref, 'fullerindiapale')

    
  def test_admin_get_reference(self):
    """
    Ensure we can create a new account object.
    """
    url = reverse('references_list')

    user = User.objects.filter(username='gerant').first()
    user.set_password('password1234')
    user.save()

    self.assertTrue(self.client.login(username='gerant', password='password1234'))

    response = self.client.get(url)

    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(Reference.objects.count(), 3)
    self.assertEqual(Reference.ref, 'leffeblonde')
    self.assertEqual(Reference.objects[1].ref, 'brewdogipa')
    self.assertEqual(Reference.objects[2].ref, 'fullerindiapale')

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

    # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    # self.assertEqual(Reference.objects.count(), 0)
    # self.assertEqual(Reference.objects[0].ref, 'leffeblonde')
    

class BarTests(APITestCase):
  fixtures = ['users_data.json', 'bars_data.json']

  def test_anonymous_get_bar(self):
    """
    Ensure we can create a new account object.
    """
    url = reverse('references_list')
    
    response = self.client.get(url)

    # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    # self.assertEqual(Reference.objects.count(), 0)
    # self.assertEqual(Reference.objects[0].ref, 'leffeblonde')
    
  def test_user_get_bar(self):
    """
    Ensure we can create a new account object.
    """
    url = reverse('references_list')
    
    self.assertTrue(self.client.login(username='user', password='userdjango'))
    
    response = self.client.get(url)

    # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    # self.assertEqual(Reference.objects.count(), 0)
    # self.assertEqual(Reference.objects[0].ref, 'leffeblonde')
    
  def test_admin_get_bar(self):
    """
    Ensure we can create a new account object.
    """
    url = reverse('references_list')
    
    self.assertTrue(self.client.login(username='admin', password='admindjango'))
    
    response = self.client.get(url)

    # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    # self.assertEqual(Reference.objects.count(), 0)
    # self.assertEqual(Reference.objects[0].ref, 'leffeblonde')

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

    # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    # self.assertEqual(Reference.objects.count(), 0)
    # self.assertEqual(Reference.objects[0].ref, 'leffeblonde')

        
class StockTests(APITestCase):
  fixtures = ['users_data.json', 'bars_data.json', 'references_data.json', 'stocks_data.json']

  def test_anonymous_get_stock(self):
    """
    Ensure we can create a new account object.
    """
    url = reverse('references_list')
    
    response = self.client.get(url)

    # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    # self.assertEqual(Reference.objects.count(), 0)
    # self.assertEqual(Reference.objects[0].ref, 'leffeblonde')
    
  def test_user_get_stock(self):
    """
    Ensure we can create a new account object.
    """
    url = reverse('references_list')
    
    self.assertTrue(self.client.login(username='user', password='userdjango'))
    
    response = self.client.get(url)

    # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    # self.assertEqual(Reference.objects.count(), 0)
    # self.assertEqual(Reference.objects[0].ref, 'leffeblonde')
    
  def test_admin_get_stock(self):
    """
    Ensure we can create a new account object.
    """
    url = reverse('references_list')
    
    self.assertTrue(self.client.login(username='admin', password='admindjango'))
    
    response = self.client.get(url)

    # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    # self.assertEqual(Reference.objects.count(), 0)
    # self.assertEqual(Reference.objects[0].ref, 'leffeblonde')

  def test_anonymous_get_menu(self):
    """
    Ensure we can create a new account object.
    """
    url = reverse('references_list')
    
    response = self.client.get(url)

    # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    # self.assertEqual(Reference.objects.count(), 0)
    # self.assertEqual(Reference.objects[0].ref, 'leffeblonde')
    
  def test_user_get_menu(self):
    """
    Ensure we can create a new account object.
    """
    url = reverse('references_list', kwargs={'pk': 1})
    
    self.assertTrue(self.client.login(username='user', password='userdjango'))
    
    response = self.client.get(url)

    # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    # self.assertEqual(Reference.objects.count(), 0)
    # self.assertEqual(Reference.objects[0].ref, 'leffeblonde')
    
  def test_admin_get_stock(self):
    """
    Ensure we can create a new account object.
    """
    url = reverse('references_list')
    
    self.assertTrue(self.client.login(username='admin', password='admindjango'))
    
    response = self.client.get(url)

    # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    # self.assertEqual(Reference.objects.count(), 0)
    # self.assertEqual(Reference.objects[0].ref, 'leffeblonde')

        
# class RankingTests(APITestCase):
#     def test_create_account(self):
#         """
#         Ensure we can create a new account object.
#         """
#         url = reverse('account-list')
#         data = {'name': 'DabApps'}
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Account.objects.count(), 1)
#         self.assertEqual(Account.objects.get().name, 'DabApps')
#
#
# class OrderTests(APITestCase):
#     def test_create_account(self):
#         """
#         Ensure we can create a new account object.
#         """
#         url = reverse('account-list')
#         data = {'name': 'DabApps'}
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Account.objects.count(), 1)
#         self.assertEqual(Account.objects.get().name, 'DabApps')
