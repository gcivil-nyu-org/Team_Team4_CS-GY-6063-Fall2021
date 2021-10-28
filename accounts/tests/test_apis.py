from django.test import SimpleTestCase
from accounts.yelp_api import yelp_search
import json
from accounts.open_data_api import open_data_query


class StudyCityAPITests(SimpleTestCase):

    def test_yelp_api_filter(self):
        test_yelp_query = yelp_search()
        params = {'location': '\xa0tandon', 'limit': 1}
        response = test_yelp_query.filter_location(params)
        resultJSON = json.loads(response)
        self.assertEqual(resultJSON['businesses'][0]['id'], 'ysqgdbSrezXgVwER2kQWKA')

    def test_yelp_api_search_business(self):
        test_yelp_query = yelp_search()
        business_id = 'gnXCEhcKF_rd5KmPUQXiYA'
        response = test_yelp_query.search_business_id(business_id)
        resultJSON = json.loads(response)
        self.assertEqual(resultJSON['id'], 'gnXCEhcKF_rd5KmPUQXiYA')

    def test_yelp_api_url(self):
        test_yelp_query = yelp_search()
        url = 'https://api.yelp.com/v3/businesses/E8RJkjfdcwgtyoPMjQ_Olg'
        response = test_yelp_query.request(url)
        resultJSON = json.loads(response)
        self.assertEqual(resultJSON['id'], 'E8RJkjfdcwgtyoPMjQ_Olg')

    def test_od_api_sanitation(self):
        name = 'The Little Sweet Cafe'
        zipcode = '11201'
        long_in = "-73.9867324 "
        lat_in = "40.6881418"
        test_od_query = open_data_query(name, zipcode, long_in, lat_in)

        response = test_od_query.sanitation_query(name, zipcode)
        resultJSON = json.loads(json.dumps(response[0]))
        self.assertEqual(resultJSON['dba'], name.upper())

    def test_od_api_three_one_one(self):
        name = 'The Little Sweet Cafe'
        zipcode = '11201'
        long_in = "-73.9867324 "
        lat_in = "40.6881418"
        test_od_query = open_data_query(name, zipcode, long_in, lat_in)

        response = test_od_query.three_one_one_query(long_in, lat_in)
        resultJSON = response[0]
        # if resultJSON:
        #     self.assertEqual(type(resultJSON['created_date']), str)
