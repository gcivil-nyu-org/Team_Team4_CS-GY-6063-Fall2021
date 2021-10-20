from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from .models import Review


class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    business_account = forms.BooleanField(required=False)  # field added to registration form

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "business_account"]


class ReviewCreateForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['user', 'yelp_id', 'business_name', 'review_text']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
