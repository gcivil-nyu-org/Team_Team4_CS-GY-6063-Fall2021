from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from .models import Review, Favorite
from crispy_forms.helper import FormHelper


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = '<i class="fas fa-envelope"></i>'
        self.fields['username'].label = '<i class="fas fa-user-circle"></i>'

    class Meta:
        model = User
        fields = ["username", "email"]
        help_texts = {
            'username': None,
            'email': None,
        }


class ProfileUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'

    class Meta:
        model = Profile
        fields = ["image"]
        labels = {"image": "<i class='fas fa-images'></i>"}
