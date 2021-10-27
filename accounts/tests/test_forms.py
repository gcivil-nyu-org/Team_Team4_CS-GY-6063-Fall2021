from django.test import SimpleTestCase
from accounts.forms import ReviewCreateForm
from django.contrib.auth.models import User


class TestForms(SimpleTestCase):
    databases = '__all__'

    def setUp(self):
        self.test_user = User.objects.create(
            username='test_user',
            email='abc@gmail.com',
            password='zh000000')

    def test_review_form(self):
        form = ReviewCreateForm(data={
            'user': self.test_user,
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
