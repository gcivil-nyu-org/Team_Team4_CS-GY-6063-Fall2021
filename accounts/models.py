from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='profile_pics/default.jpg', upload_to='profile_pics')
    business_account = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} Profile'


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    yelp_id = models.CharField(max_length=256)
    review_text = models.CharField(max_length=512)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user.username} review {self.yelp_id} as {self.review_text} on {self.date_posted}'
