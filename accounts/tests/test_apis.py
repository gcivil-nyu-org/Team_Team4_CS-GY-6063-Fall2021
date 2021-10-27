from django.test import SimpleTestCase
from accounts.yelp_api import yelp_search
import json
# from accounts.open_data_api import  open_data_query

class StudyCityAPITests(SimpleTestCase):

    def test_yelp_api(self):
        test_yelp_query = yelp_search()
        business_id = 'gnXCEhcKF_rd5KmPUQXiYA'
        params = {'location': '\xa0tandon', 'limit': 1}
        url = 'https://api.yelp.com/v3/businesses/E8RJkjfdcwgtyoPMjQ_Olg'

        response = test_yelp_query.filter_location(params)
        resultJSON = json.loads(response)
        print("TEST", resultJSON)
        self.assertEqual(resultJSON['businesses'][0]['id'], 'ysqgdbSrezXgVwER2kQWKA')

        response = test_yelp_query.search_business_id(business_id)
        resultJSON = json.loads(response)
        self.assertEqual(resultJSON['id'], 'gnXCEhcKF_rd5KmPUQXiYA')
 
        response = test_yelp_query.request(url)
        resultJSON = json.loads(response)
        self.assertEqual(resultJSON['id'], 'E8RJkjfdcwgtyoPMjQ_Olg')

    # def test_open_data_api(self):
    #     pass
