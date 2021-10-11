from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    username = models.CharField(max_length=256)
    email = models.CharField(max_length=256)
    business_account = models.BooleanField(default=False)
    def __str__(self):
        return self
    def set(self, username, email, business_account):
        self.username = username
        self.email = email
        self.business_account = business_account