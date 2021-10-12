from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='profile_pics/default.jpg', upload_to='profile_pics')
    # username = models.CharField(max_length=256)
    # email = models.CharField(max_length=256)
    # business_account = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} Profile'
    # def set(self, username, email, business_account):
    #     self.username = username
    #     self.email = email
    #     self.business_account = business_account
