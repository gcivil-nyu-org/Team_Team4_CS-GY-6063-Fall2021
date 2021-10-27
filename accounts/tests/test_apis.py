from django.test import SimpleTestCase
from accounts.yelp_api import yelp_search
import json
# from accounts.open_data_api import  open_data_query

class StudyCityAPITests(SimpleTestCase):

    def test_yelp_api(self):
        test_yelp_query = yelp_search()

        # term = 'tandon'
        # location = 'new york'
        # business_id = 'E8RJkjfdcwgtyoPMjQ_Olg'
        # params = {'location': '\\xa0tandon', 'limit': 25}
        url = 'https://api.yelp.com/v3/businesses/E8RJkjfdcwgtyoPMjQ_Olg'

        # response = test_yelp_query.search_location(term, location)
        # print(response)
        # self.assertEqual(response.status_code, 200)
        
        # response = test_yelp_query.filter_location(params)
        # print(response)
        # self.assertEqual(response.status_code, 200)

        # response = test_yelp_query.search_business_id(business_id)
        # self.assertEqual(response.status_code, 200)
 
        output = test_yelp_query.request(url)
        resultJSON = json.loads(output)
        self.assertEqual(resultJSON['id'], 'E8RJkjfdcwgtyoPMjQ_Olg')

    def test_open_data_api(self):
        pass
