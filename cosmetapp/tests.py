from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import NumberPhone

class SignUpLoginTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_signup_view(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 302)

    def test_edit_profile_view(self):
        response = self.client.get(reverse('edit_profile'))
        self.assertEqual(response.status_code, 200)

    def test_delete_account_view(self):
        response = self.client.get(reverse('delete_account'))
        self.assertEqual(response.status_code, 200)

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 302)

    def test_logout_view(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  

class OrderTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_add_order_view(self):
        response = self.client.get(reverse('add_order'))
        self.assertEqual(response.status_code, 200)

    def test_orders_by_request_user(self):
        response = self.client.get(reverse('orders'))
        self.assertEqual(response.status_code, 200)

class NumberPhoneTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_add_number_phone_view(self):
        response = self.client.get(reverse('add_number_phone'))
        self.assertEqual(response.status_code, 200)

    def test_update_number_phone_view(self):
        phone_number = NumberPhone.objects.create(user=self.user, number_phone='123456789')
        response = self.client.get(reverse('update_number_phone', args=[phone_number.pk]))
        self.assertEqual(response.status_code, 200)

    def test_number_phone_by_request_user(self):
        response = self.client.get(reverse('number_phone'))
        self.assertEqual(response.status_code, 200)