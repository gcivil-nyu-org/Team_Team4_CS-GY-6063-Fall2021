from django.test import SimpleTestCase
from django.urls import reverse, resolve
from django.template.loader import render_to_string
from accounts.views import index, registerPage, \
    logoutUser, profile, locationDetail


class StudyCityURLTests(SimpleTestCase):

    def test_url_index(self):
        url = reverse('index')
        self.assertEquals(resolve(url).func, index)

    def test_url_register(self):
        url = reverse('register')
        self.assertEquals(resolve(url).func, registerPage)

    def test_url_logout(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func, logoutUser)

    def test_url_profile(self):
        url = reverse('profile')
        self.assertEquals(resolve(url).func, profile)

    def test_url_location_detail(self):
        url = reverse('locationDetail')
        self.assertEquals(resolve(url).func, locationDetail)

    def test_url_password_reset(self):
        with self.assertTemplateUsed(template_name='accounts/password_reset.html'):
            render_to_string('accounts/password_reset.html')

    def test_url_password_reset_done(self):
        with self.assertTemplateUsed(template_name='accounts/password_reset_done.html'):
            render_to_string('accounts/password_reset_done.html')

    def test_url_password_reset_confirm(self):
        with self.assertTemplateUsed(template_name='accounts/password_reset_confirm.html'):
            render_to_string('accounts/password_reset_confirm.html')

    def test_url_password_reset_complete(self):
        with self.assertTemplateUsed(template_name='accounts/password_reset_complete.html'):
            render_to_string('accounts/password_reset_complete.html')
