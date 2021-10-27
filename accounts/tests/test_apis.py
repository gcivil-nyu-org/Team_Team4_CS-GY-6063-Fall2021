from unittest.main import TestProgram
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from accounts.yelp_api import open_data_query
from accounts.open_data_api import yelp_search

class StudyCityAPITests(SimpleTestCase):

    def test_yelp_api(self):
        test_yelp_query = yelp_search()


        term = 'tandon'
        location = 'new york'
        business_id = 'E8RJkjfdcwgtyoPMjQ_Olg'
        params = {'location': '\\xa0tandon', 'limit': 25}
        url = 'https://api.yelp.com/v3/businesses/E8RJkjfdcwgtyoPMjQ_Olg'

        
        response = self.test_yelp_query.search_location(term, location)
        self.assertEqual(response.status_code, 200)
        
        response = self.test_yelp_query.filter_location(params)
        self.assertEqual(response.status_code, 200)

        response = self.test_yelp_query.search_business_id(business_id)
        self.assertEqual(response.status_code, 200)

        response = self.test_yelp_query.request(url)
        self.assertEqual(response.status_code, 200)
     
    def test_open_data_api(self):
        pass
