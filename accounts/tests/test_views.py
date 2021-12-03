from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from accounts.models import Review, Favorite
from accounts.zip_codes import zipcodeInNYC, filterInNYC, noNYCResults


class StudyCityViewsTests(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(username='testuser', email="abcd@gmail.com")
        self.user.set_password('123456e')
        self.user.save()
        self.c = Client()

    def test_index_Get(self):
        response = self.c.get(reverse('index'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/index.html')

    def test_profile_Get(self):
        logged_in = self.c.login(username='testuser', password='123456e')
        self.assertTrue(logged_in)
        response = self.c.get(reverse('profile'))
        self.assertEquals(response.status_code, 200)

    def test_location_Get(self):
        logged_in = self.c.login(username='testuser', password='123456e')
        self.assertTrue(logged_in)
        response = self.c.get(reverse('locationDetail') +
                              '?locationID=uks5xzzN5F88a3OOibkYLg')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/location_detail.html')

    def test_index_all(self):
        logged_in = self.c.login(username='testuser', password='123456e')
        self.assertTrue(logged_in)
        searchURL = reverse('index')
        data = {'place': ['11201'], 'longitude': [''], 'latitude': [''], 'open_now': ['on'], 'rating': ['5'],
                'price': ['2'], 'comfort': ['5'], 'food': ['5'], 'wifi': ['5'], 'charging': ['5']}
        response = self.c.get(searchURL, data)
        self.assertEquals(response.status_code, 200)
        test_user = User.objects.create(
            username='test_user',
            email='xyz@gmail.com',
            password='ss000000'
        )
        test_user.save()
        review = Review.objects.create(
            user=test_user,
            yelp_id='sTQJwv9dQlAEF5RhLGgEaA',
            review_text='good',
            wifi_rating=3,
            general_rating=3,
            food_rating=3,
            comfort_rating=3,
            charging_rating=4,
        )
        review.save()
        data = {'place': [''], 'useCurrentLocation': ['true'], 'longitude': ['-73.9848232'], 'latitude': ['40.6893135'],
                'open_now': ['on'], 'rating': ['4'], 'price': [''], 'comfort': ['4'], 'food': ['4'], 'wifi': ['4'], 'charging': ['4']}
        response = self.c.get(searchURL, data)
        self.assertEquals(response.status_code, 200)

    def test_index_place(self):
        searchURL = reverse('index') + '?place=tandon'
        response = self.c.post(searchURL)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/index.html')

    def test_index_with_currentLocation(self):
        searchURL = reverse(
            'index') + '/?place=&useCurrentLocation=true& \
            longitude=-73.9846658&latitude=40.6918129'
        response = self.c.post(searchURL)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/index.html')

    def test_favorite_Post(self):
        logged_in = self.c.login(username='testuser', password='123456e')
        self.assertTrue(logged_in)
        yelp_id = 'uks5xzzN5F88a3OOibkYLg'
        yelp_name = 'Jill Lindsey'
        location_detail_url = reverse('locationDetail') + '?locationID=' + yelp_id
        response = self.c.post(location_detail_url,
                               {'fav_locationid': yelp_id, 'fav_locationname': yelp_name})
        self.assertEquals(response.status_code, 302)
        favorite = Favorite.objects.get(user=self.user, yelp_id=yelp_id)
        self.assertEquals(favorite.business_name, yelp_name)

        response = self.c.post(location_detail_url,
                               {'fav_locationid': yelp_id,
                                'fav_locationname': yelp_name,
                                'unfavorite': "1",
                                })
        favorite_list = Favorite.objects.filter(user=self.user, yelp_id=yelp_id)
        self.assertEquals(favorite_list.count(), 0)

    def test_review_Post(self):
        logged_in = self.c.login(username='testuser', password='123456e')
        self.assertTrue(logged_in)
        yelp_id = 'uks5xzzN5F88a3OOibkYLg'
        yelp_name = 'Jill Lindsey'
        before_review_post_count = Review.objects.filter(
            user=self.user, yelp_id=yelp_id).count()
        location_detail_url = reverse('locationDetail') + '?locationID=' + yelp_id
        review_post = {
            "locationid": yelp_id,
            "locationname": yelp_name,
            "review": "Good place to go!",
            "wifi_rating": 5,
            "general_rating": 5,
            "food_rating": 4,
            "comfort_rating": 3,
            "charging_rating": 4,
        }
        response = self.c.post(location_detail_url,
                               review_post)
        self.assertEquals(response.status_code, 302)
        after_review_post_count = Review.objects.filter(
            user=self.user, yelp_id=yelp_id).count()
        self.assertEquals(before_review_post_count + 1, after_review_post_count)

    def test_login(self):
        logged_in = self.c.login(username='testuser', password='123456e')
        self.assertTrue(logged_in)
        response = self.c.get(reverse('profile'))
        # user_info = {"username": "testuser", "password": "123456e"}
        # self.c.post(reverse("login"), user_info)
        # response = self.c.get(reverse('logout'))
        self.assertEquals(response.status_code, 200)

    def test_profile1_Get(self):
        logged_in = self.c.login(username='testuser', password='123456e')
        self.assertTrue(logged_in)
        response = self.c.get(reverse('profile'))
        self.assertEquals(response.status_code, 200)

    def test_zipcodeInNYC(self):
        zipcode = '10001'
        item = {}
        zipcodeInNYC(item, zipcode)
        self.assertEquals(item['in_nyc'], True)

    def test_filterInNYC(self):
        item = {}
        item['in_nyc'] = True
        response = filterInNYC(item)
        self.assertEquals(response, True)

    def test_noNYCResults(self):
        empty_list = []
        response = noNYCResults(empty_list)
        self.assertEquals(response, True)

    def test_aboutPage(self):
        response = self.c.get(reverse('about'))
        self.assertEquals(response.status_code, 200)

    def test_checkout_success(self):
        response = self.c.get(reverse('checkout_success'))
        self.assertEquals(response.status_code, 200)

    def test_checkout_cancel(self):
        response = self.c.get(reverse('checkout_cancel'))
        self.assertEquals(response.status_code, 200)
