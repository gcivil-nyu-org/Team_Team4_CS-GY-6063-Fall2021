from .models import BProfile, Profile
from .yelp_api import Yelp_Search
import datetime
import json
#from dateutil.relativedelta import relativedelta
# question - does is_promoted bool flip to false once end date passes?

class AdClients:
    
    def __init__(self):
        self.today = self.todays_date()
        self.client_list = self.get_ad_clients()
        self.client_data = self.get_yelp_info(self.client_list)

    def todays_date(self):
        # YYYY-MM-DD HH:MM:SS
        date = datetime.date.today() #now()
        return date

    # get list of advertising clientele and return User profiles
    def get_ad_clients(self):
        # pull database object if is_promoted is True -> return BProfile objects
        ad_clients = BProfile.objects.filter(is_promoted=True)
        client_profiles = []

        # loop over result and extract respective User objects
        for client in ad_clients:
            # if advertising window is still live for client, append to list
            if client.promote_start_date <= self.today and self.today <= client.promote_end_date:
                # get the user's Profile instance from their User instance
                profile = Profile.objects.get(user=client.user)
                client_profiles.append(profile)

        return client_profiles
        
    def get_yelp_info(self, client_profiles):
        # loop over client profiles and build yelp info list for ad clients
        yelp_search_obj = Yelp_Search()

        client_data = []
        for client in client_profiles:
            yelp_info = yelp_search_obj.search_business_id(client.verified_yelp_id)
            yelp_info_JSON = json.loads(yelp_info)
            #yelp_info_JSON['promoted'] = True
            client_data.append(yelp_info_JSON)

        return client_data

