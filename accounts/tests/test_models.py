from django.test import TestCase
from accounts.models import Profile, Review, Favorite
from django.contrib.auth.models import User


class TestModels(TestCase):
    def test_profile(self):
        test_user = User.objects.create(
            username='test_user',
            email='xyz@gmail.com',
            password='ss000000'
        )
        prof = Profile.objects.get(user=test_user)
        print(prof)
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
        print(review)
        self.assertEquals(review.yelp_id,"abcd")
        self.assertEquals(review.review_text,"good")
        self.assertEquals(review.wifi_rating,3)
        self.assertEquals(review.general_rating,4)
        self.assertEquals(review.food_rating,5)
        self.assertEquals(review.comfort_rating,4)
        self.assertEquals(review.charging_rating,5)

# user = models.ForeignKey(User, on_delete=models.CASCADE)
#     yelp_id = models.CharField(max_length=256)
#     business_name = models.CharField(max_length=64, default="StudySpace")
#     date_posted = models.DateTimeField(default=timezone.now)

#     def __str__(self):
#         return f"{self.business_name} is {self.user.username}'s favorite"

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
        print(fav)
        # user_prof=Favorite.objects.get(user=test_user)
        self.assertEquals(fav.yelp_id,"abcd")
        