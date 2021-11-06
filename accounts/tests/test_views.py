from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from accounts.models import Review, Favorite


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
        response = self.c.get(reverse('user'))
        self.assertEquals(response.status_code, 200)
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
        data = {'place': [''], 'useCurrentLocation': ['true'], 'longitude': ['-73.9848464'], 'latitude': ['40.689306'], 'open_now': ['on'], 'rating': ['5'], 'price': ['2'], 'comfort': ['5'], 'food': ['5'], 'wifi': ['5'], 'charging': ['4']}
        response = self.c.get(searchURL, data)
        self.assertEquals(response.status_code, 200)
        data = {'place': ['11201'], 'longitude': [''], 'latitude': [''], 'open_now': ['on'], 'rating': ['5'], 'price': ['2'], 'comfort': ['5'], 'food': ['5'], 'wifi': ['5'], 'charging': ['5']}
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
        self.assertEquals(response.status_code, 200)
        favorite = Favorite.objects.get(user=self.user, yelp_id=yelp_id)
        self.assertEquals(favorite.business_name, yelp_name)

        response = self.c.post(location_detail_url,
                               {'fav_locationid': yelp_id, 'fav_locationname': yelp_name})
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
        self.assertEquals(response.status_code, 200)
        after_review_post_count = Review.objects.filter(
            user=self.user, yelp_id=yelp_id).count()
        self.assertEquals(before_review_post_count + 1, after_review_post_count)

    def test_login(self):
        logged_in = self.c.login(username='testuser', password='123456e')
        self.assertTrue(logged_in)
        response = self.c.get(reverse('user'))
        # user_info = {"username": "testuser", "password": "123456e"}
        # self.c.post(reverse("login"), user_info)
        # response = self.c.get(reverse('logout'))
        self.assertEquals(response.status_code, 200)

    def test_profile1_Get(self):
        logged_in = self.c.login(username='testuser', password='123456e')
        self.assertTrue(logged_in)
        response = self.c.get(reverse('profile'))
        self.assertEquals(response.status_code, 200)

    # def test_register(self):
    #     user_info = {"username": "testuser1",
    #                  "email": "abcdef@gmail.com",
    #                  "password1": "test000000",
    #                  "password2": "test000000",
    #                  "business_account": True}
    #     print(reverse("register"))
    #     response = self.c.post(reverse("register"), user_info)
    #     self.assertEquals(response.status_code, 200)
    #     logged_in = self.c.login(username='testuser1', password='test000000')
    #     self.assertTrue(logged_in)

