import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.db.models import Sum, Count

from .models import Reference, Bar, Stock, Order


# Tests URLs for references.
class ReferenceTests(APITestCase):
    fixtures = ['users_data.json', 'references_data.json']

    def setUp(self):
        """
        Initialization of parameter by default.
        """

        self.data_post = {
            "ref": "chouffeblonde",
            "name": "La Chouffe Blonde",
            "description": "Bière dorée légèrement trouble à mousse dense, avec un parfum épicé aux notes d’agrumes et de coriandre qui ressortent également au goût."
        }

        # User password initialization
        user = User.objects.filter(username='barman').first()
        user.set_password('password1234')
        user.save()

        user = User.objects.filter(username='gerant').first()
        user.set_password('password1234')
        user.save()

    def test_anonymous_get_reference(self):
        """
        Ensure an anonymous user can not access to references.
        """
        url = reverse('references_list')

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_get_reference(self):
        """
        Ensure that an authenticated user can access to references.
        """
        url = reverse('references_list')

        # User connection
        self.assertTrue(self.client.login(username='barman', password='password1234'))

        response = self.client.get(url)
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response['count'], Reference.objects.all().count())

        # Verification that each returned reference is in the database
        for result in json_response['results']:
            ref_reference = result['ref']
            name_reference = result['name']
            description_reference = result['description']

            self.assertEqual(Reference.objects.filter(ref=ref_reference).count(), 1)

            reference = Reference.objects.filter(ref=ref_reference).first()

            self.assertEqual(name_reference, reference.name)
            self.assertEqual(description_reference, reference.description)

        self.client.logout()

    def test_admin_get_reference(self):
        """
        Ensure that an admin user can access to references.
        """
        url = reverse('references_list')

        # User connection
        self.assertTrue(self.client.login(username='gerant', password='password1234'))

        response = self.client.get(url)
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response['count'], Reference.objects.all().count())

        # Verification that each returned reference is in the database
        for result in json_response['results']:
            ref_reference = result['ref']
            name_reference = result['name']
            description_reference = result['description']

            self.assertEqual(Reference.objects.filter(ref=ref_reference).count(), 1)

            reference = Reference.objects.filter(ref=ref_reference).first()

            self.assertEqual(name_reference, reference.name)
            self.assertEqual(description_reference, reference.description)

        self.client.logout()

    def test_anonymous_post_reference(self):
        """
        Ensure an anonymous user can not create a new reference object.
        """
        url = reverse('references_list')

        response = self.client.post(url, self.data_post, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_post_reference(self):
        """
        Ensure an authenticated user can not create a new reference object.
        """
        url = reverse('references_list')

        # User connection
        self.assertTrue(self.client.login(username='barman', password='password1234'))

        response = self.client.post(url, self.data_post, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.logout()

    def test_admin_post_reference(self):
        """
        Ensure an admin user can create a new reference object.
        """
        url = reverse('references_list')

        # User connection
        self.assertTrue(self.client.login(username='gerant', password='password1234'))

        # Post new reference
        response = self.client.post(url, self.data_post, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(url)
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response['count'], Reference.objects.all().count())

        # Verification that the new reference is added to the list
        new_reference_find = [result for result in json_response['results'] if self.data_post['ref'] == result['ref']]
        self.assertEqual(len(new_reference_find), 1)

        self.client.logout()


# Tests URLs for bars.
class BarTests(APITestCase):
    fixtures = ['users_data.json', 'bars_data.json']

    def setUp(self):
        """
        Initialization of parameter by default.
        """

        self.data_post = {
            "name": "3ème comptoir"
        }

        # User password initialization
        user = User.objects.filter(username='barman').first()
        user.set_password('password1234')
        user.save()

        user = User.objects.filter(username='gerant').first()
        user.set_password('password1234')
        user.save()

    def test_anonymous_get_bar(self):
        """
        Ensure an anonymous user can not access to bars.
        """
        url = reverse('bars_list')

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_get_bar(self):
        """
        Ensure that an authenticated user can access to bars.
        """
        url = reverse('bars_list')

        # User connection
        self.assertTrue(self.client.login(username='barman', password='password1234'))

        response = self.client.get(url)
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response['count'], Bar.objects.all().count())

        # Verification that each returned bar is in the database
        for result in json_response['results']:
            pk_bar = result['id']
            name_bar = result['name']

            self.assertEqual(Bar.objects.filter(pk=pk_bar).count(), 1)

            bar = Bar.objects.filter(pk=pk_bar).first()

            self.assertEqual(name_bar, bar.name)

        self.client.logout()

    def test_admin_get_bar(self):
        """
        Ensure that an admin user can access to references.
        """
        url = reverse('bars_list')

        # User connection
        self.assertTrue(self.client.login(username='gerant', password='password1234'))

        response = self.client.get(url)
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response['count'], Bar.objects.all().count())

        # Verification that each returned bar is in the database
        for result in json_response['results']:
            pk_bar = result['id']
            name_bar = result['name']

            self.assertEqual(Bar.objects.filter(pk=pk_bar).count(), 1)

            bar = Bar.objects.filter(pk=pk_bar).first()

            self.assertEqual(name_bar, bar.name)

        self.client.logout()

    def test_anonymous_post_bar(self):
        """
        Ensure an anonymous user can not create a new bar object.
        """
        url = reverse('bars_list')

        response = self.client.post(url, self.data_post, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_post_bar(self):
        """
        Ensure an authenticated user can not create a new bar object.
        """
        url = reverse('bars_list')

        # User connection
        self.assertTrue(self.client.login(username='barman', password='password1234'))

        response = self.client.post(url, self.data_post, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.logout()

    def test_admin_post_bar(self):
        """
        Ensure an admin user can create a new bar object.
        """
        url = reverse('bars_list')

        # User connection
        self.assertTrue(self.client.login(username='gerant', password='password1234'))

        # Post new bar
        response = self.client.post(url, self.data_post, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(url)
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response['count'], Bar.objects.all().count())

        # Verification that the new bar is added to the list
        new_stock_find = [result for result in json_response['results'] if self.data_post['name'] == result['name']]
        self.assertEqual(len(new_stock_find), 1)

        self.client.logout()


# Tests URLs for stocks.
class StockTests(APITestCase):
    fixtures = ['users_data.json', 'bars_data.json', 'references_data.json', 'stocks_data.json']

    def setUp(self):
        """
        Initialization of parameter by default.
        """

        self.data_post = {
            "reference": 3,
            "stock": 15
        }

        self.default_bar = 1

        # User password initialization
        user = User.objects.filter(username='barman').first()
        user.set_password('password1234')
        user.save()

        user = User.objects.filter(username='gerant').first()
        user.set_password('password1234')
        user.save()

    def test_anonymous_get_stock(self):
        """
        Ensure an anonymous user can not access to stock of bar.
        """
        url = reverse('stock_detail', args=(self.default_bar,))

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_get_stock(self):
        """
        Ensure that an authenticated user can access to stock of bar.
        """

        # User connection
        self.assertTrue(self.client.login(username='barman', password='password1234'))

        # Route of all bars
        for bar in Bar.objects.all():
            url = reverse('stock_detail', args=(bar.pk,))

            response = self.client.get(url)
            json_response = json.loads(response.content)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(json_response['count'], Stock.objects.filter(bar=bar.pk).count())

            # Verification that each returned stock is in the database
            for result in json_response['results']:
                ref_reference = result['ref']
                name_reference = result['name']
                description_reference = result['description']
                stock_reference = result['stock']

                self.assertEqual(Stock.objects.filter(reference__ref=ref_reference, bar=bar.pk).count(), 1)

                stock = Stock.objects.filter(reference__ref=ref_reference, bar=bar.pk).first()

                self.assertEqual(name_reference, stock.reference.name)
                self.assertEqual(description_reference, stock.reference.description)
                self.assertEqual(stock_reference, stock.stock)

        self.client.logout()

    def test_admin_get_stock(self):
        """
        Ensure we can create a new account object.
        """

        # User connection
        self.assertTrue(self.client.login(username='gerant', password='password1234'))

        # Route of all bars
        for bar in Bar.objects.all():
            url = reverse('stock_detail', args=(bar.pk,))

            response = self.client.get(url)
            json_response = json.loads(response.content)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(json_response['count'], Stock.objects.filter(bar=bar.pk).count())

            # Verification that each returned stock is in the database
            for result in json_response['results']:
                ref_reference = result['ref']
                name_reference = result['name']
                description_reference = result['description']
                stock_reference = result['stock']

                self.assertEqual(Stock.objects.filter(reference__ref=ref_reference, bar=bar.pk).count(), 1)

                stock = Stock.objects.filter(reference__ref=ref_reference, bar=bar.pk).first()

                self.assertEqual(name_reference, stock.reference.name)
                self.assertEqual(description_reference, stock.reference.description)
                self.assertEqual(stock_reference, stock.stock)

        self.client.logout()

    def test_anonymous_post_stock(self):
        """
        Ensure an anonymous user can not create a new bar object.
        """
        url = reverse('stock_detail', args=(self.default_bar,))

        response = self.client.post(url, self.data_post, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_post_stock(self):
        """
        Ensure an authenticated user can not create a new bar object.
        """
        url = reverse('stock_detail', args=(self.default_bar,))

        # User connection
        self.assertTrue(self.client.login(username='barman', password='password1234'))

        response = self.client.post(url, self.data_post, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.logout()

    def test_admin_post_stock(self):
        """
        Ensure an admin user can create update a stock object.
        """
        url = reverse('stock_detail', args=(self.default_bar,))

        # User connection
        self.assertTrue(self.client.login(username='gerant', password='password1234'))

        # Check of the current stock
        response = self.client.get(url)
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response['count'], Stock.objects.filter(bar=self.default_bar).count())

        stocks_before_post = [result['stock'] for result in json_response['results'] if
                              result['ref'] == Stock.objects.filter(reference=self.data_post['reference'],
                                                                    bar=self.default_bar).first().reference.ref]
        self.assertEqual(len(stocks_before_post), 1)
        self.assertEqual(stocks_before_post[0], 0)

        # Update of the stock
        response = self.client.post(url, self.data_post, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check of the updated stock
        response = self.client.get(url)
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response['count'], Stock.objects.filter(bar=self.default_bar).count())

        stocks_after_post = [result['stock'] for result in json_response['results'] if
                             result['ref'] == Stock.objects.filter(reference=self.data_post['reference'],
                                                                   bar=self.default_bar).first().reference.ref]
        self.assertEqual(len(stocks_after_post), 1)
        self.assertEqual(stocks_after_post[0], self.data_post['stock'])

        self.client.logout()


# Tests URLs for the menu.
class MenuTests(APITestCase):
    fixtures = ['users_data.json', 'bars_data.json', 'references_data.json', 'stocks_data.json']

    def setUp(self):
        """
        Initialization of parameter by default.
        """

        # User password initialization
        user = User.objects.filter(username='barman').first()
        user.set_password('password1234')
        user.save()

        user = User.objects.filter(username='gerant').first()
        user.set_password('password1234')
        user.save()

    def test_anonymous_get_all_menu(self):
        """
        Ensure an anonymous user can access to menu.
        """
        url = reverse('menu_list')

        response = self.client.get(url)
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verification of the availability of each reference
        for result in json_response['results']:
            ref_reference = result['ref']
            availability = result['availability']

            self.assertEqual(Reference.objects.filter(ref=ref_reference).annotate(total_stock=Sum('stocks__stock')).count(), 1)

            reference = Reference.objects.filter(ref=ref_reference).annotate(total_stock=Sum('stocks__stock')).first()

            if reference.total_stock > 0:
                self.assertEqual(availability, 'available')
            else:
                self.assertEqual(availability, 'outofstock')

    def test_anonymous_get_bar_menu(self):
        """
        Ensure an anonymous user can access to menu of bar.
        """

        # Route of all bars
        for bar in Bar.objects.all():
            url = reverse('menu_detail', args=(bar.pk,))

            response = self.client.get(url)
            json_response = json.loads(response.content)

            self.assertEqual(response.status_code, status.HTTP_200_OK)

            # Verification of the availability of each reference
            for result in json_response['results']:
                ref_reference = result['ref']
                availability = result['availability']

                self.assertEqual(Reference.objects.filter(ref=ref_reference, stocks__bar__pk=bar.pk).annotate(
                    total_stock=Sum('stocks__stock')).count(), 1)

                reference = Reference.objects.filter(ref=ref_reference, stocks__bar__pk=bar.pk).annotate(
                    total_stock=Sum('stocks__stock')).first()

                if reference.total_stock > 0:
                    self.assertEqual(availability, 'available')
                else:
                    self.assertEqual(availability, 'outofstock')

    def test_user_get_all_menu(self):
        """
        Ensure an authenticated user can access to menu.
        """
        url = reverse('menu_list')

        # User connection
        self.assertTrue(self.client.login(username='barman', password='password1234'))

        response = self.client.get(url)
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verification of the availability of each reference
        for result in json_response['results']:
            ref_reference = result['ref']
            availability = result['availability']

            self.assertEqual(
                Reference.objects.filter(ref=ref_reference).annotate(total_stock=Sum('stocks__stock')).count(), 1)

            reference = Reference.objects.filter(ref=ref_reference).annotate(total_stock=Sum('stocks__stock')).first()

            if reference.total_stock > 0:
                self.assertEqual(availability, 'available')
            else:
                self.assertEqual(availability, 'outofstock')

        self.client.logout()

    def test_user_get_bar_menu(self):
        """
        Ensure an authenticated user can access to menu of bar.
        """

        # User connection
        self.assertTrue(self.client.login(username='barman', password='password1234'))

        # Route of all bars
        for bar in Bar.objects.all():
            url = reverse('menu_detail', args=(bar.pk,))

            response = self.client.get(url)
            json_response = json.loads(response.content)

            self.assertEqual(response.status_code, status.HTTP_200_OK)

            # Verification of the availability of each reference
            for result in json_response['results']:
                ref_reference = result['ref']
                availability = result['availability']

                self.assertEqual(Reference.objects.filter(ref=ref_reference, stocks__bar__pk=bar.pk).annotate(
                    total_stock=Sum('stocks__stock')).count(), 1)

                reference = Reference.objects.filter(ref=ref_reference, stocks__bar__pk=bar.pk).annotate(
                    total_stock=Sum('stocks__stock')).first()

                if reference.total_stock > 0:
                    self.assertEqual(availability, 'available')
                else:
                    self.assertEqual(availability, 'outofstock')

        self.client.logout()

    def test_admin_get_all_menu(self):
        """
        Ensure an admin user can access to menu.
        """
        url = reverse('menu_list')

        # User connection
        self.assertTrue(self.client.login(username='gerant', password='password1234'))

        response = self.client.get(url)
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verification of the availability of each reference
        for result in json_response['results']:
            ref_reference = result['ref']
            availability = result['availability']

            self.assertEqual(
                Reference.objects.filter(ref=ref_reference).annotate(total_stock=Sum('stocks__stock')).count(), 1)

            reference = Reference.objects.filter(ref=ref_reference).annotate(total_stock=Sum('stocks__stock')).first()

            if reference.total_stock > 0:
                self.assertEqual(availability, 'available')
            else:
                self.assertEqual(availability, 'outofstock')

        self.client.logout()

    def test_admin_get_bar_menu(self):
        """
        Ensure an admin user can access to menu of bar.
        """

        # User connection
        self.assertTrue(self.client.login(username='gerant', password='password1234'))

        # Route of all bars
        for bar in Bar.objects.all():
            url = reverse('menu_detail', args=(bar.pk,))

            response = self.client.get(url)
            json_response = json.loads(response.content)

            self.assertEqual(response.status_code, status.HTTP_200_OK)

            # Verification of the availability of each reference
            for result in json_response['results']:
                ref_reference = result['ref']
                availability = result['availability']

                self.assertEqual(Reference.objects.filter(ref=ref_reference, stocks__bar__pk=bar.pk).annotate(
                    total_stock=Sum('stocks__stock')).count(), 1)

                reference = Reference.objects.filter(ref=ref_reference, stocks__bar__pk=bar.pk).annotate(
                    total_stock=Sum('stocks__stock')).first()

                if reference.total_stock > 0:
                    self.assertEqual(availability, 'available')
                else:
                    self.assertEqual(availability, 'outofstock')

        self.client.logout()


# Tests URLs for the ranking.
class RankingTests(APITestCase):
    fixtures = ['users_data.json', 'bars_data.json', 'references_data.json', 'stocks_data.json']

    def setUp(self):
        """
        Initialization of parameter by default.
        """

        # User password initialization
        user = User.objects.filter(username='barman').first()
        user.set_password('password1234')
        user.save()

        user = User.objects.filter(username='gerant').first()
        user.set_password('password1234')
        user.save()

    def test_anonymous_get_ranking(self):
        """
        Ensure an anonymous user can not access to ranking.
        """
        url = reverse('ranking_list')

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_get_ranking(self):
        """
        Ensure an authenticated user can access to ranking.
        """

        url = reverse('ranking_list')

        # User connection
        self.assertTrue(self.client.login(username='barman', password='password1234'))

        response = self.client.get(url)
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Recovery in database of bar informations
        bars_all = Bar.objects.exclude(stocks__stock=0).distinct()
        bars_miss = Bar.objects.filter(stocks__stock=0).distinct()
        bar_most = Bar.objects.annotate(total_order=Count('orders__orderItems')).order_by('-total_order').first()

        self.assertEqual(len(json_response[0]['bars']), len(bars_all))
        self.assertEqual(len(json_response[1]['bars']), len(bars_miss))
        self.assertEqual(json_response[2]['bars'][0], bar_most.pk)

        # Check of the returned informations
        index = 0
        for bar in bars_all:
            self.assertEqual(json_response[0]['bars'][index], bar.pk)
            index += 1

        index = 0
        for bar in bars_miss:
            self.assertEqual(json_response[1]['bars'][index], bar.pk)
            index += 1

        self.client.logout()

    def test_admin_get_ranking(self):
        """
        Ensure an admin user can access to ranking.
        """

        url = reverse('ranking_list')

        # User connection
        self.assertTrue(self.client.login(username='gerant', password='password1234'))

        response = self.client.get(url)
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Recovery in database of bar informations
        bars_all = Bar.objects.exclude(stocks__stock=0).distinct()
        bars_miss = Bar.objects.filter(stocks__stock=0).distinct()
        bar_most = Bar.objects.annotate(total_order=Count('orders__orderItems')).order_by('-total_order').first()

        self.assertEqual(len(json_response[0]['bars']), len(bars_all))
        self.assertEqual(len(json_response[1]['bars']), len(bars_miss))
        self.assertEqual(json_response[2]['bars'][0], bar_most.pk)

        # Check of the returned informations
        index = 0
        for bar in bars_all:
            self.assertEqual(json_response[0]['bars'][index], bar.pk)
            index += 1

        index = 0
        for bar in bars_miss:
            self.assertEqual(json_response[1]['bars'][index], bar.pk)
            index += 1

        self.client.logout()


# Tests URLs for orders.
class OrderTests(APITestCase):
    fixtures = ['users_data.json', 'bars_data.json', 'references_data.json', 'stocks_data.json']

    def setUp(self):
        """
        Initialization of parameter by default.
        """

        self.data_post_1 = {
            "items": [
                {"ref": "fullerindiapale"},
                {"ref": "brewdogipa"},
                {"ref": "leffeblonde"},
                {"ref": "fullerindiapale"},
            ]
        }

        self.data_post_2 = {
            "items": [
                {"ref": "brewdogipa"},
                {"ref": "brewdogipa"},
                {"ref": "leffeblonde"},
                {"ref": "leffeblonde"},
            ]
        }
        self.default_bar = 1
        self.default_data = self.data_post_1

        # User password initialization
        user = User.objects.filter(username='barman').first()
        user.set_password('password1234')
        user.save()

        user = User.objects.filter(username='gerant').first()
        user.set_password('password1234')
        user.save()

    def test_anonymous_get_list_orders(self):
        """
        Ensure an anonymous user can not access to the list of orders.
        """
        url = reverse('order_list')

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_get_list_orders(self):
        """
        Ensure that an authenticated user can access to the list of orders.
        """
        url = reverse('order_list')

        # User connection
        self.assertTrue(self.client.login(username='barman', password='password1234'))

        response = self.client.get(url)
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response['count'], Order.objects.all().count())

        # Verification that each returned order is in the database
        for result in json_response['results']:
            pk_order = result['pk']

            self.assertEqual(Order.objects.filter(pk=pk_order).count(), 1)

        self.client.logout()

    def test_admin_get_list_orders(self):
        """
        Ensure that an admin user can access to the list of orders.
        """
        url = reverse('order_list')

        # User connection
        self.assertTrue(self.client.login(username='gerant', password='password1234'))

        response = self.client.get(url)
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response['count'], Order.objects.all().count())

        # Verification that each returned order is in the database
        for result in json_response['results']:
            pk_order = result['pk']

            self.assertEqual(Order.objects.filter(pk=pk_order).count(), 1)

        self.client.logout()

    def test_anonymous_post_order(self):
        """
        Ensure an anonymous user can create a new order.
        """
        url = reverse('order_detail', args=(self.default_bar,))

        response = self.client.post(url, self.default_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_post_order(self):
        """
        Ensure an authenticated user can not create a new order.
        """
        url = reverse('order_detail', args=(self.default_bar,))

        # User connection
        self.assertTrue(self.client.login(username='barman', password='password1234'))

        response = self.client.post(url, self.default_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.logout()

    def test_admin_post_order(self):
        """
        Ensure an admin user can not create a new order.
        """
        url = reverse('order_detail', args=(self.default_bar,))

        # User connection
        self.assertTrue(self.client.login(username='gerant', password='password1234'))

        response = self.client.post(url, self.default_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.logout()

    def test_admin_get_order_detail(self):
        """
        Verification that orders are saved in database.
        """
        # Simulation of several orders
        self.default_bar = 1
        self.default_data = self.data_post_1
        OrderTests.test_anonymous_post_order(self)

        self.default_bar = 1
        self.default_data = self.data_post_2
        OrderTests.test_anonymous_post_order(self)

        self.default_bar = 2
        self.default_data = self.data_post_1
        OrderTests.test_anonymous_post_order(self)

        self.default_bar = 2
        self.default_data = self.data_post_2
        OrderTests.test_anonymous_post_order(self)

        self.default_bar = 2
        self.default_data = self.data_post_1
        OrderTests.test_anonymous_post_order(self)

        # Verification of the order list
        OrderTests.test_admin_get_list_orders(self)

        # User connection
        self.assertTrue(self.client.login(username='gerant', password='password1234'))

        # Verification of the content of order number 3
        url = reverse('order_detail', args=(3,))

        response = self.client.get(url)
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response['bar'], self.default_bar)
        self.assertEqual(len(json_response['orderItems']), 4)

        # Verification informations of bars
        RankingTests.test_admin_get_ranking(self)

        self.client.logout()

