from django.test import SimpleTestCase
from django.urls import reverse, resolve
from accounts.views import index, loginPage, registerPage, \
                           logoutUser, user, profile, locationDetail
#from accounts.templates.accounts import password_reset
                        

class StudyCityURLTests(SimpleTestCase):

    def test_url_index(self):
        url = reverse('index')
        print(resolve(url))
        self.assertEquals(resolve(url).func, index)

    
    def test_url_login(self):
        url = reverse('login')
        print(resolve(url))
        self.assertEquals(resolve(url).func, loginPage)


    def test_url_register(self):
        url = reverse('register')
        print(resolve(url))
        self.assertEquals(resolve(url).func, registerPage)


    def test_url_logout(self):
        url = reverse('logout')
        print(resolve(url))
        self.assertEquals(resolve(url).func, logoutUser)


    def test_url_user(self):
        url = reverse('user')
        print(resolve(url))
        self.assertEquals(resolve(url).func, user)


    def test_url_profile(self):
        url = reverse('profile')
        print(resolve(url))
        self.assertEquals(resolve(url).func, profile)


    def test_url_location_detail(self):
        url = reverse('locationDetail')
        print(resolve(url))
        self.assertEquals(resolve(url).func, locationDetail)
