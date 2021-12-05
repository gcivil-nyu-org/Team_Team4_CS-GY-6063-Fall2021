from .models import User, Profile, BProfile
import datetime


class AdClients:

    def __init__(self, item):
        self.item = item
        self.name = item['name']
        self.id = item['id']

    def check_if_advertising(self):
        try:
            profile = Profile.objects.get(verified_yelp_id=self.id)
            if profile is not None:
                try:
                    user = User.objects.get(profile=profile)
                except User.DoesNotExist:
                        self.item['advertising'] = False
                        return False
                try: 
                    bprofile = BProfile.objects.get(user=user)
                    if bprofile.is_promoted:
                        today = datetime.date.today()
                        if bprofile.promote_start_date <= today and \
                            today <= bprofile.promote_end_date:
                            self.item['advertising'] = True
                            return True
                        elif self.today > bprofile.promote_end_date:
                            # if ad window expired, set is_promoted to False
                            bprofile.is_promoted = False
                            return False
                except BProfile.DoesNotExist:
                    self.item['advertising'] = False
                    return False

        except Profile.DoesNotExist:
            self.item['advertising'] = False
            return False