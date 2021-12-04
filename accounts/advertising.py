from .models import User, Profile, BProfile
import datetime

# question - does is_promoted bool flip to false once end date passes?
class AdClients:

    def __init__(self, item):
        self.item = item
        self.name = item['name']
        self.id = item['id']
        self.today = self.todays_date()

    def todays_date(self):
        # YYYY-MM-DD HH:MM:SS
        date = datetime.date.today()
        return date

    def check_if_advertisting(self):
        try:
            profile = Profile.objects.get(verified_yelp_id=self.id)
            if profile is not None:
                try:
                    user = User.objects.get(profile=profile)
                except User.DoesNotExist:
                        self.item['advertising'] = False
                try: 
                    bprofile = BProfile.objects.get(user=user)
                    if bprofile.is_promoted == True:
                        if bprofile.promote_start_date <= self.today and \
                            self.today <= bprofile.promote_end_date:
                            self.item['advertising'] = True
                except BProfile.DoesNotExist:
                    self.item['advertising'] = False

        except Profile.DoesNotExist:
            self.item['advertising'] = False