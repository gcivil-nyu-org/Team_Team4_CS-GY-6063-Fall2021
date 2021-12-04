from django.test import SimpleTestCase
from accounts.forms import ReviewCreateForm, FavoriteCreateForm, RegisterForm
from django.contrib.auth.models import User


class TestForms(SimpleTestCase):
    databases = '__all__'

    # def setUp(self):

    def test_review_form(self):
        test_user = User.objects.create(
            username='test_user',
            email='abc@gmail.com',
            password='zh000000')
        form = ReviewCreateForm(data={
            'user': test_user,
            'yelp_id': 'abcdefg',
            'business_name': 'cafe star',
            'review_text': 'Good place to go!',
            'wifi_rating': 5,
            'general_rating': 4,
            'comfort_rating': 3,
            'food_rating': 4,
            'charging_rating': 5
        })
        self.assertTrue(form.is_valid())

    def test_favorite_form(self):
        test_user = User.objects.create(
            username='test_user1',
            email='abc1@gmail.com',
            password='zh000000')
        form = FavoriteCreateForm(data={
            'user': test_user,
            'yelp_id': 'abcdefg',
            'business_name': 'cafe star'
        })
        self.assertTrue(form.is_valid())

    # def test_register_form_clean(self):
    #     form = RegisterForm(data={
    #             'username': 'test_user2',
    #             'email': 'abcd@gmail.com',
    #             'password1': 'zh000000',
    #             'password2': 'zh000000',
    #             'business_account': False
    #     })

    #     form2 = RegisterForm(data={
    #             'username': 'test_user3',
    #             'email': 'abcd@gmail.com',
    #             'password1': 'zh000001',
    #             'password2': 'zh000001',
    #             'business_account': False
    #     })

    #     self.assertTrue(form.is_valid())
    #     self.assertTrue(form2.is_valid())