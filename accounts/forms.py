from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from .models import Review, Favorite


class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    business_account = forms.BooleanField(
        required=False
    )  # field added to registration form

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "business_account"]


class ReviewCreateForm(forms.ModelForm):
    review_text = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = Review
        fields = [
            "user",
            "yelp_id",
            "business_name",
            "review_text",
            "wifi_rating",
            "general_rating",
            "comfort_rating",
            "food_rating",
            "charging_rating",
        ]


class FavoriteCreateForm(forms.ModelForm):
    class Meta:
        model = Favorite
        fields = ["user", "yelp_id", "business_name"]


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email"]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["image"]

class BusinessProfileForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields='__all__'

class BusinessUpdate(forms.ModelForm):
    class Meta:
        model=Profile
        fields=["image","address","phone","business_hours"]

