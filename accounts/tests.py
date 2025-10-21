from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterForm
from django.core import mail

User = get_user_model()


class AuthenticationTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }
        self.user = User.objects.create_user(
            username='existinguser',
            first_name='Existing',
            last_name='User',
            email='existing@example.com',
            password='testpass123'
        )

    def test_register_view_get(self):
        """Test register view GET request"""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Register')
        self.assertIsInstance(response.context['form'], UserCreationForm)

    def test_register_view_post_valid(self):
        """Test successful user registration"""
        response = self.client.post(reverse('register'), self.user_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_register_view_post_invalid(self):
        """Test registration with invalid data"""
        invalid_data = self.user_data.copy()
        invalid_data['password2'] = 'different_password'
        response = self.client.post(reverse('register'), invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='testuser').exists())

    def test_login_view_get(self):
        """Test login view GET request"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Login')

    def test_login_view_post_valid(self):
        """Test successful login"""
        login_data = {
            'username': 'existing@example.com',  # Use email as username
            'password': 'testpass123'
        }
        response = self.client.post(reverse('login'), login_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.endswith('/dashboard/'))

    def test_login_view_post_invalid(self):
        """Test login with invalid credentials"""
        login_data = {
            'username': 'existinguser',
            'password': 'wrongpassword'
        }
        response = self.client.post(reverse('login'), login_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Login')

    def test_dashboard_requires_login(self):
        """Test that dashboard requires authentication"""
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)
        # Check if it redirects to login (could be /login/ or /accounts/login/)
        self.assertTrue(response.url.startswith('/login/') or response.url.startswith('/accounts/login/'))

    def test_dashboard_authenticated(self):
        """Test dashboard access for authenticated user"""
        self.client.login(username='existing@example.com', password='testpass123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome, existinguser!')

    def test_logout_view(self):
        """Test logout functionality"""
        self.client.login(username='existing@example.com', password='testpass123')
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.endswith('/login/'))


class RegisterFormTestCase(TestCase):
    def test_register_form_valid(self):
        """Test RegisterForm with valid data"""
        form_data = {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'new@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }
        form = RegisterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_register_form_invalid_email(self):
        """Test RegisterForm with invalid email"""
        form_data = {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'invalid-email',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_register_form_password_mismatch(self):
        """Test RegisterForm with password mismatch"""
        form_data = {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'new@example.com',
            'password1': 'testpass123',
            'password2': 'differentpass'
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())


class PasswordResetTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            first_name='Test',
            last_name='User',
            email='test@example.com',
            password='testpass123'
        )

    def test_password_reset_view(self):
        """Test password reset view"""
        response = self.client.get(reverse('password_reset'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Reset Your Password')

    def test_password_reset_post(self):
        """Test password reset form submission"""
        response = self.client.post(reverse('password_reset'), {
            'email': 'test@example.com'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Password reset', mail.outbox[0].subject)
