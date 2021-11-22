from django.test import TestCase
from accounts.filters import Checks
from accounts.models import User, Review

class StudyCityFiltersTests(TestCase):

    def test_Checks(self):
        item = {}
        item['name'] = 'test_business'

        test_user = User.objects.create(
            username='test_user',
            email='xyz@gmail.com',
            password='ss000000'
        )

        test_review = Review.objects.create(
                user=test_user,
                yelp_id='abcd',
                business_name='test_business',
                review_text='good', 
                comfort_rating=4,
                food_rating=4,
                wifi_rating=4,
                charging_rating=4,
                general_rating=4
        )

        checks_obj = Checks(item, 5, 5, 5, 5)
        checks_obj.perform_checks()

        self.assertEqual(item['comfort'], 4)
        self.assertEqual(item['food'], 4)
        self.assertEqual(item['wifi'], 4)
        self.assertEqual(item['charging'], 4)
        
