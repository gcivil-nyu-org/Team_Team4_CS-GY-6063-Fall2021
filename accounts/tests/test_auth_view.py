from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from accounts.utils import account_activation_token


class BaseTest(TestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.user = {
            'email': 'testemail@gmail.com',
            'username': 'username',
            'password': 'password',
            'password2': 'password',
        }
        self.user_short_password = {
            'email': 'testemail@gmail.com',
            'username': 'username',
            'password': 'tes',
            'password2': 'tes',
        }
        self.user_unmatching_password = {

            'email': 'testemail@gmail.com',
            'username': 'username',
            'password': 'teslatt',
            'password2': 'teslatto',
        }

        self.user_invalid_email = {

            'email': 'test.com',
            'username': 'username',
            'password': 'teslatt',
            'password2': 'teslatto',
        }
        return super().setUp()


class RegisterTest(BaseTest):
    def test_can_view_page_correctly(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_can_register_user(self):
        response = self.client.post(self.register_url, self.user, format='text/html')
        self.assertEqual(response.status_code, 200)


class LoginTest(BaseTest):
    def test_can_view_page_correctly(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_login_success(self):
        user = User.objects.create_user('testuser', 'crytest@gmail.com')
        user.set_password('tetetebvghhhhj')
        user.is_active = True
        user.save()
        response = self.client.post(
            self.login_url, {'username': 'testuser', 'password': 'acbddfsd'}, format='text/html')
        self.assertEqual(response.status_code, 200)


class UserVerifyTest(BaseTest):
    def test_user_ctivates_success(self):
        user = User.objects.create_user('testuser', 'crytest@gmail.com')
        user.set_password('tetetebvghhhhj')
        user.is_active = False
        user.save()
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)
        response = self.client.get(
            reverse('activate', kwargs={'uidb64': uid, 'token': token}))
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(email='crytest@gmail.com')
        self.assertTrue(user.is_active)

    def test_user_cant_ctivates_succesfully(self):
        user = User.objects.create_user('testuser', 'crytest@gmail.com')
        user.set_password('tetetebvghhhhj')
        user.is_active = False
        user.save()
        response = self.client.get(
            reverse('activate', kwargs={'uidb64': 'uid', 'token': 'token'}))
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(email='crytest@gmail.com')
        self.assertFalse(user.is_active)

    def test_user_already_active(self):
        user = User.objects.create_user('testuser', 'crytest@gmail.com')
        user.set_password('tetetebvghhhhj')
        user.is_active = True
        user.save()
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)
        response = self.client.get(
            reverse('activate', kwargs={'uidb64': uid, 'token': token}))
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(email='crytest@gmail.com')
        self.assertTrue(user.is_active)
