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

    '''
    # will add back once coordinate front-end with Leo
    def check_311(self):
        if queryStr.get('311_check'):
            open_data_object = open_data_query(name, zipcode, long_in, lat_in)
            open_data_threeoneone = json.loads(
                json.dumps(open_data_object.three_one_one))
        
            # check whether 311 query returns, if yes render value
            if (open_data_threeoneone[0]['created_date'] == 'NA'):
                item['check_311'] = True
            else:
                item['check_311'] = False
    '''

class Filters():
    
    def __init__(self, response, comfort, food, wifi, charging):
        self.response = response
        self.comfort = comfort
        self.food = food
        self.wifi = wifi
        self.charging = charging
        self.attribute = ''
        self.argument = 0

    def filter_all(self):
        if self.comfort:
            self.attribute = 'comfort'
            self.argument = self.comfort
            self.response = list(filter(self.goe_filter, self.response))
        if self.food:
            self.attribute = 'food'
            self.argument = self.food
            self.response = list(filter(self.goe_filter, self.response))
        if self.wifi:
            self.attribute = 'wifi'
            self.argument = self.wifi
            self.response = list(filter(self.goe_filter, self.response))
        if self.charging:
            self.attribute = 'charging'
            self.argument = self.charging
            self.response = list(filter(self.goe_filter, self.response))
        return self.response

    def goe_filter(self, item):
        return int(item[self.attribute]) >= int(self.argument)

    '''
    # will add back once coordinate front-end with Leo
    Comment 311, by Hang
    def filterBy311(item):
        if (item['check_311']):
            return True

    Comment 311, by Hang
    def filterBy311(item):
        if (item['check_311']):
            return True
    if queryStr.get('311_check'):
        response = list(filter(filterBy311, response))
    '''

