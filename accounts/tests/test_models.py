from django.test import TestCase
from accounts.models import Profile, Review, Favorite
from django.contrib.auth.models import User
from populate import populate_test_accounts


class TestModels(TestCase):
    def test_profile(self):
        test_user = User.objects.create(
            username='test_user',
            email='xyz@gmail.com',
            password='ss000000'
        )
        prof = Profile.objects.get(user=test_user)
        self.assertFalse(prof.business_account)

    def test_review(self):
        test_user = User.objects.create(
            username='test_user',
            email='xyz@gmail.com',
            password='ss000000'
        )
        review = Review.objects.create(
            user=test_user,
            yelp_id='abcd',
            review_text='good', 
            wifi_rating=3, 
            general_rating=4,
            food_rating=5,
            comfort_rating=4,
            charging_rating=5,
            )

        self.assertEquals(review.yelp_id,"abcd")
        self.assertEquals(review.review_text,"good")
        self.assertEquals(review.wifi_rating,3)
        self.assertEquals(review.general_rating,4)
        self.assertEquals(review.food_rating,5)
        self.assertEquals(review.comfort_rating,4)
        self.assertEquals(review.charging_rating,5)

    def test_favorites(self):
        test_user = User.objects.create(
            username='test_user',
            email='xyz@gmail.com',
            password='ss000000'
        )
        fav = Favorite.objects.create(
            user=test_user,
            yelp_id='abcd',   
        )

        self.assertEquals(fav.yelp_id,"abcd")

    
    def test_populate_test_accounts(self):
        populate_test_accounts()
        user_name = 'prof_test'
        user = User.objects.get(username=user_name)
        is_business = Profile.objects.get(user=user).business_account
        self.assertEquals(is_business, True)