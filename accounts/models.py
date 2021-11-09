from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(
        default="profile_pics/default.jpg", upload_to="profile_pics"
    )
    business_account = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} Profile"


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    yelp_id = models.CharField(max_length=256)
    business_name = models.CharField(max_length=64, default="StudySpace")
    review_text = models.CharField(max_length=512)
    wifi_rating = models.IntegerField(default=0)
    general_rating = models.IntegerField(default=0)
    food_rating = models.IntegerField(default=0)
    charging_rating = models.IntegerField(default=0)
    comfort_rating = models.IntegerField(default=0)
    date_posted = models.DateTimeField(default=timezone.now)
    
    class Meta:
         unique_together = ('user','yelp_id')
    

    def __str__(self):
        
        return f"{self.user.username} \
                reviewed {self.business_name} \
                as {self.review_text} \
                on {self.date_posted}"
    

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    yelp_id = models.CharField(max_length=256)
    business_name = models.CharField(max_length=64, default="StudySpace")
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.business_name} is {self.user.username}'s favorite"
