# sanitation points https://a816-health.nyc.gov/ABCEatsRestaurants/#!/faq

from sodapy import Socrata
import os

class open_data_query:

    def __init__(self, name, zipcode, long_in, lat_in):
        self.open_data_key = os.environ.get("OD_APP_TOKEN")
        self.client = Socrata("data.cityofnewyork.us", self.open_data_key)
        self.name = name
        self.zipcode = zipcode
        self.long_in = long_in
        self.lat_in = lat_in
        self.sanitation = self.sanitation_query(self.name, self.zipcode)
        self.three_one_one = self.three_one_one_query(self.long_in, self.lat_in)

    def sanitation_query(self, name, zipcode):
        name_upper = name.upper()
        where_input = "(dba='" + name_upper + "') and (zipcode='" + zipcode + "') and (grade!='is null')"

        req = self.client.get("43nn-pn8j", select="dba, grade, score, grade_date, violation_description", where=where_input, order="grade_date DESC", limit = 1)
        if req:
            return req
        else:
            return "NA"

    def three_one_one_query(self, long_in, lat_in):
        # return queries that are within ~25 meters square of location's coordinates
        proximity = 0.00025
        long_float = float(long_in)
        lat_float = float(lat_in)

        long_top = long_float + proximity
        long_bot = long_float - proximity
        lat_top = lat_float + proximity
        lat_bot = lat_float - proximity

        where_input = "(longitude between " + str(long_bot) + " and " + str(long_top) + ")" \
              " and (latitude between " + str(lat_bot) + " and " + str(lat_top) + ")" \
              " and (status= 'Open' or status= 'In Progress' )"

        req = self.client.get("erm2-nwe9", select="complaint_type, descriptor, \
                  intersection_street_1, intersection_street_2, status", \
                  where=where_input, limit = 5)
        
        if req:
            return req
        else:
            return "NA"