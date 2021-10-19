from django.contrib import admin
from .models import Profile, Review

# simple profile model
# class ProfileAdmin(admin.ModelAdmin):
#     model = Profile
#     # list_display = ['user']

# admin.site.register(Profile, ProfileAdmin)
admin.site.register(Profile)
admin.site.register(Review)
