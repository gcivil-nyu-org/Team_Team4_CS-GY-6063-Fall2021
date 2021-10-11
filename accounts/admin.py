from django.contrib import admin
from .models import Profile

# simple profile model
class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ('username', 'email', 'business_account')

admin.site.register(Profile, ProfileAdmin)