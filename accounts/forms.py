from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, BProfile
from .models import Review, Favorite
from crispy_forms.helper import FormHelper
from django.contrib.auth.forms import PasswordResetForm

class EmailValidationOnForgotPassword(PasswordResetForm):

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            msg = ("There is no user registered with the specified E-Mail address.")
            self.add_error('email', msg)
        return email


class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    business_account = forms.BooleanField(
        required=False
    )  # field added to registration form

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "business_account"]

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            msg = 'A user with that email already exists.'
            self.add_error('email', msg)

        return self.cleaned_data


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
    # email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['email'].label = '<i class="fas fa-envelope me-1"></i> Username'
        self.fields['username'].label = '<i class="fas fa-user-circle me-1"></i> Username'

    class Meta:
        model = User
        fields = ["username"]
        help_texts = {
            'username': None,
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
        labels = {"image": "<i class='fas fa-images me-1'></i> Avatar"}


class BusinessProfileForm(forms.ModelForm):
    class Meta:
        model = BProfile
        fields = ["user"]
        # print("BPF")
        # fields="__all__"


class BusinessUpdate(forms.ModelForm):
    class Meta:
        model = BProfile
        # fields=["address","phone","business_hours"]
        fields = ["image", "address", "phone", "business_hours"]
