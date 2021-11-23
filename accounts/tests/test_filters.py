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

        checks_obj = Checks(item, 5, 5, 5, 5)
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
                       'rating': 4.5, 
                       'coordinates': {'latitude': 41.089991, 'longitude': -74.013422}, 
                       'transactions': ['delivery', 'pickup'], 
                       'location': {'address1': '199 Main St', 
                                    'address2': None, 
                                    'address3': '', 
                                    'city': 'Nanuet', 
                                    'zip_code': '10954', 
                                    'country': 'US', 
                                    'state': 'NY', 
                                    'display_address': ['199 Main St', 
                                                        'Nanuet, NY 10954']}, 
                       'phone': '+18454423017', 
                       'display_phone': '(845) 442-3017', 
                       'distance': 39929.28767391573, 
                       'in_nyc': False, 
                       'comfort': 5, 
                       'food': 5, 
                       'wifi': 5, 
                       'charging': 5}]

        filters = Filters(response, 4, 4, 4, 4)
        response = filters.filter_all()

        self.assertEquals(response[0]['comfort'], 5)
        self.assertEqual(response[0]['food'], 5)
        self.assertEqual(response[0]['wifi'], 5)
        self.assertEqual(response[0]['charging'], 5)

