import os
import requests
import json

class yelp_search:

    def __init__(self):
        self.yelp_api_key = os.environ.get("YELP_API_KEY")
        self.headers = {'Authorization': 'Bearer %s' % self.yelp_api_key}
    
    def search_location(self, term, location):
        params = {'term':term, 'location':location} 
        url = 'https://api.yelp.com/v3/businesses/search'
        self.request(url, params)

    def search_business_id(self, business_id):
        url = 'https://api.yelp.com/v3/businesses/' + business_id
        self.request(url)

    def request(self, url, search_params=None):
        # get request
        req = requests.get(url, params=search_params, headers=self.headers)
        # proceed only if the status code is 200
        status_code = req.status_code
        if req.status_code == 200:
            parsed = json.loads(req.text)
            output = json.dumps(parsed, indent=4)
            # for terminal testing
            print(output)
        else:
            print("search error (see yelp_api.py):", status_code)
        # return json object
        return output
        
