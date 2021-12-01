from django.test import TestCase
from accounts.filters import Checks, Filters
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

        review = Review.objects.create(
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
        review.save()

        checks_obj = Checks(item, 5, 5, 5, 5, False)
        checks_obj.perform_checks()

        self.assertEqual(item['comfort'], 4)
        self.assertEqual(item['food'], 4)
        self.assertEqual(item['wifi'], 4)
        self.assertEqual(item['charging'], 4)
    
    def test_Filters(self):
        response = [{'id': 'sTQJwv9dQlAEF5RhLGgEaA', 'alias': 
                       'eat-study-and-sip-nanuet', 'name': 'Eat Study & Sip',
                       'review_count': 25, 
                       'categories': [{'alias': 'cafes', 'title': 'Cafes'}], 
                       'rating': 5,
                       'comfort': 5, 
                       'food': 5, 
                       'wifi': 5, 
                       'charging': 5,
                       'check_311': False}]

        filters = Filters(response, 4, 4, 4, 4, 4, False)
        response = filters.filter_all()

        self.assertEquals(response[0]['comfort'], 5)
        self.assertEqual(response[0]['food'], 5)
        self.assertEqual(response[0]['wifi'], 5)
        self.assertEqual(response[0]['charging'], 5)
        self.assertEqual(response[0]['rating'], 5)
        self.assertEqual(response[0]['check_311'], False)
