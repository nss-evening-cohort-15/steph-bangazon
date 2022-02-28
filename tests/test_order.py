from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.core.management import call_command
from django.contrib.auth.models import User

from bangazon_api.models import Order, Product, PaymentType


class OrderTests(APITestCase):
    def setUp(self):
        """
        Seed the database
        """
        call_command('seed_db', user_count=3)
        self.user1 = User.objects.filter(store=None).first()
        self.token = Token.objects.get(user=self.user1)
        # self.payment_type = PaymentType.objects.get(customer=self.user1)

        product = Product.objects.get(pk=1)

        self.order1 = Order.objects.create(
            user=self.user1,
        )

        self.order1.products.add(product)
 

        # self.order1.payment_type = self.payment_type

        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.token.key}')

        self.faker = Faker()

    def test_list_orders(self):
        """The orders list should return a list of orders for the logged in user"""
        response = self.client.get('/api/orders')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(len(response.data), Order.objects.count(user=self.user1))

    def test_delete_order(self):
        """
        Ensure order can be deleted
        """
        response = self.client.delete(f'/api/orders/{self.order1.id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_complete_order(self):
        """Adding a payment type should complete the order"""

        # data = {
        #     "merchant": self.faker.credit_card_provider(),
        #     "acctNumber": self.faker.credit_card_number()
        # }

        response = self.client.put(f'api/orders/{self.order1.id}/complete')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # response = self.client.put(f'api/orders/{self.order1.id}/complete', data, format='json')
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertIsNotNone(response.data['id'])
        # self.assertEqual(response.data["merchant_name"], data['merchant'])
        # self.assertEqual(response.data["acct_number"], data['acctNumber'])

        # response = self.client.get('/api/orders')
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
    