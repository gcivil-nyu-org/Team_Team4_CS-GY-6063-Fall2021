from .models import Review
from django.db.models import Avg

class Checks():
        # abstracted way to check update item object based on query inputs
        def __init__(self, item, comfort, food, wifi, charging):
            self.item = item
            self.name = item['name']
            self.comfort = comfort
            self.food = food
            self.wifi = wifi
            self.charging = charging
           
        def perform_checks(self):
            self.check_comfort()
            self.check_food()
            self.check_wifi()
            self.check_charging()

        def check_comfort(self):
            if self.comfort:
                try:
                    # pull database object for location (i.e., item)
                    db_rating = Review.objects.filter(business_name=self.name).aggregate(Avg('comfort_rating'))[
                        'comfort_rating__avg']
                    if db_rating is not None:
                        self.item['comfort'] = int(db_rating)
                    else:
                        self.item['comfort'] = 0
                except IndexError:
                    self.item['comfort'] = 0

        def check_food(self):
            if self.food:
                try:
                    # pull database object for location (i.e., item)
                    db_rating = Review.objects.filter(business_name=self.name).aggregate(Avg('food_rating'))[
                        'food_rating__avg']
                    if db_rating is not None:
                        self.item['food'] = int(db_rating)
                    else:
                        self.item['food'] = 0
                except IndexError:
                    self.item['food'] = 0

        def check_wifi(self):
            if self.wifi:
                try:
                    # pull database object for location (i.e., item)
                    db_rating = Review.objects.filter(business_name=self.name).aggregate(Avg('wifi_rating'))[
                        'wifi_rating__avg']
                    if db_rating is not None:
                        self.item['wifi'] = int(db_rating)
                    else:
                        self.item['wifi'] = 0
                except IndexError:
                    self.item['wifi'] = 0

        def check_charging(self):
            if self.charging:
                try:
                    # pull database object for location (i.e., item)
                    db_rating = Review.objects.filter(business_name=self.name).aggregate(Avg('charging_rating'))[
                        'charging_rating__avg']
                    if db_rating is not None:
                        self.item['charging'] = int(db_rating)
                    else:
                        self.item['charging'] = 0
                except IndexError:
                    self.item['charging'] = 0
        