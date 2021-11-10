from django.contrib import admin
from .models import Profile, Review, Favorite


class ProfileAdmin(admin.ModelAdmin):
    readonly_fields = ()
    admin_readonly_fields = ('claimed_business_name', 'verified_yelp_id', 'verified')

    def get_readonly_fields(self, request, obj=Profile):
        if obj.business_account:
            return super(ProfileAdmin, self).get_readonly_fields(request, obj=obj)
        else:
            return self.admin_readonly_fields

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Review)
admin.site.register(Favorite)
