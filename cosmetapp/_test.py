import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from .models import NumberPhone

# Fixture
@pytest.fixture
def client(db):
    from django.test import Client
    return Client()

@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser', password='testpassword')

@pytest.fixture
def logged_in_client(client, user):
    client.login(username='testuser', password='testpassword')
    return client

# Testy dla rejestracji i logowania (SignUpLoginTests)
def test_signup_view(client):
    response = client.get(reverse('signup'))
    assert response.status_code == 200

def test_edit_profile_view(logged_in_client):
    response = logged_in_client.get(reverse('edit_profile'))
    assert response.status_code == 200

def test_delete_account_view(logged_in_client):
    response = logged_in_client.get(reverse('delete_account'))
    assert response.status_code == 200

def test_login_view(client):
    response = client.get(reverse('login'))
    assert response.status_code == 200

def test_logout_view(logged_in_client):
    response = logged_in_client.get(reverse('logout'))
    assert response.status_code == 302  # Powinno przekierować na stronę logowania

# Testy dla zamówień (OrderTests)
def test_order_add_order_view(logged_in_client):
    response = logged_in_client.get(reverse('add_order'))
    assert response.status_code == 200

def test_order_orders_by_request_user(logged_in_client):
    response = logged_in_client.get(reverse('orders'))
    assert response.status_code == 200

# Testy dla numerów telefonów (NumberPhoneTests)
def test_number_phone_add_number_phone_view(logged_in_client):
    response = logged_in_client.get(reverse('add_number_phone'))
    assert response.status_code == 200

def test_number_phone_update_number_phone_view(logged_in_client, user):
    phone_number = NumberPhone.objects.create(user=user, number_phone='123456789')
    response = logged_in_client.get(reverse('update_number_phone', args=[phone_number.pk]))
    assert response.status_code == 200

def test_number_phone_by_request_user(logged_in_client):
    response = logged_in_client.get(reverse('number_phone'))
    assert response.status_code == 200