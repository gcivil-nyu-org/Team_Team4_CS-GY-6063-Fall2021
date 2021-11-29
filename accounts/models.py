from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from datetime import datetime


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(
        default="profile_pics/default.jpg", upload_to="profile_pics"
    )
    business_account = models.BooleanField(default=False)
    claimed_business_name = models.CharField(max_length=256, blank=True, default="")
    verified_yelp_id = models.CharField(
        max_length=256, blank=True, default="", unique=True)
    verified = models.BooleanField(default=False)
    email_confirmed = models.BooleanField(default=False)
    

    def save(self, *args, **kwargs):
        if not self.business_account:
            self.verified = False
            now = str(datetime.now())
            self.claimed_business_name = "last modified: " + now
            self.verified_yelp_id = "last modified: " + now
        super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} Profile"


class BProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # image = models.ImageField(
    #     default="profile_pics/default.jpg", upload_to="profile_pics"
    # )
    # business_account = models.BooleanField(default=False)
    # claimed_business_name = models.CharField(max_length=256, blank=True, default="")
    # verified_yelp_id = models.CharField(
    #     max_length=256, blank=True, default="", unique=True)
    # verified = models.BooleanField(default=False)
    # email_confirmed = models.BooleanField(default=False)
    address=models.TextField(max_length=256, blank=True, default="")
    phone=models.CharField(max_length=64, blank=True,default="")
    business_hours=models.CharField(max_length=256,blank=True,default="")
      

    # def save(self, *args, **kwargs):
    #     if not self.business_account:
    #         self.verified = False
    #         now = str(datetime.now())
    #         self.claimed_business_name = "last modified: " + now
    #         self.verified_yelp_id = "last modified: " + now
    #     super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} BProfile"


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    yelp_id = models.CharField(max_length=256)
    business_name = models.CharField(max_length=64, default="StudySpace")
    review_text = models.TextField(max_length=256,blank=True)
    wifi_rating = models.IntegerField(default=0)
    general_rating = models.IntegerField(default=0)
    food_rating = models.IntegerField(default=0)
    charging_rating = models.IntegerField(default=0)
    comfort_rating = models.IntegerField(default=0)
    date_posted = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'yelp_id')

    def get_absolute_url(self):
        return reverse('review-update-suc')

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
