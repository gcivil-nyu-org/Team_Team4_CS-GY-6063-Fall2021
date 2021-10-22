
from sodapy import Socrata
import os
import json


class open_data_query:

    def __init__(self):
        self.open_data_key = os.environ.get("OD_APP_TOKEN")
        self.client = Socrata("data.cityofnewyork.us", self.open_data_key)
    
    def sanitation_query(self, long_in, lat_in):
        req = self.client.get("43nn-pn8j", longitude=long_in, latitude=lat_in, limit = 1)
        # output = json.dumps(req, indent=4)
        output = {"name": str(req[0]['dba']),  
                 "grade": str(req[0]['grade']),
                 "grade date": str(req[0]['grade_date']), 
                 "inspection date": str(req[0]['inspection_date']),
                 "actions": str(req[0]['action']),
                 "violation_description": str(req[0]['violation_description'])}

        for k, v in output:
            print(k, ":", v)

        return output

    def three_one_one_query(self, long_in, lat_in):
        # return queries that are within ~25 meters of location's coordinates
        proximity = 0.00025
        long_top = long_in + proximity
        long_bot = long_in - proximity
        lat_top = lat_in + proximity
        lat_bot = lat_in - proximity

        where_input = "(longitude between " + str(long_bot) + " and " + str(long_top) + ")" \
              " and (latitude between " + str(lat_bot) + " and " + str(lat_top) + ")" \
              " and (status= 'Open' or status= 'In Progress' )"

        req2 = self.client.get("erm2-nwe9", select="complaint_type, descriptor, \
                  intersection_street_1, intersection_street_2, status", \
                  where=where_input, limit = 10)
        
        output = json.dumps(req2, indent=4)
        print(output)