from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.template.defaultfilters import slugify
import re

# using slugify to create unique values if business account is removed
def unique_slugify(instance, value, slug_field_name='slug', queryset=None,
                   slug_separator='-'):
    """
    Calculates and stores a unique slug of ``value`` for an instance.

    ``slug_field_name`` should be a string matching the name of the field to
    store the slug in (and the field to check against for uniqueness).

    ``queryset`` usually doesn't need to be explicitly provided - it'll default
    to using the ``.all()`` queryset from the model's default manager.
    """
    slug_field = instance._meta.get_field(slug_field_name)

    slug = getattr(instance, slug_field.attname)
    slug_len = slug_field.max_length

    # Sort out the initial slug, limiting its length if necessary.
    slug = slugify(value)
    if slug_len:
        slug = slug[:slug_len]
    slug = _slug_strip(slug, slug_separator)
    original_slug = slug

    # Create the queryset if one wasn't explicitly provided and exclude the
    # current instance from the queryset.
    if queryset is None:
        queryset = instance.__class__._default_manager.all()
    if instance.pk:
        queryset = queryset.exclude(pk=instance.pk)

    # Find a unique slug. If one matches, at '-2' to the end and try again
    # (then '-3', etc).
    next = 2
    while not slug or queryset.filter(**{slug_field_name: slug}):
        slug = original_slug
        end = '%s%s' % (slug_separator, next)
        if slug_len and len(slug) + len(end) > slug_len:
            slug = slug[:slug_len-len(end)]
            slug = _slug_strip(slug, slug_separator)
        slug = '%s%s' % (slug, end)
        next += 1

    setattr(instance, slug_field.attname, slug)

def _slug_strip(value, separator='-'):
    """
    Cleans up a slug by removing slug separator characters that occur at the
    beginning or end of a slug.

    If an alternate separator is used, it will also replace any instances of
    the default '-' separator with the new separator.
    """
    separator = separator or ''
    if separator == '-' or not separator:
        re_sep = '-'
    else:
        re_sep = '(?:-|%s)' % re.escape(separator)
    # Remove multiple instances and if an alternate separator is provided,
    # replace the default '-' separator.
    if separator != re_sep:
        value = re.sub('%s+' % re_sep, separator, value)
    # Remove separator from the beginning and end of the slug.
    if separator:
        if separator != '-':
            re_sep = re.escape(separator)
        value = re.sub(r'^%s+|%s+$' % (re_sep, re_sep), '', value)
    return value

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(
        default="profile_pics/default.jpg", upload_to="profile_pics"
    )
    business_account = models.BooleanField(default=False)
    claimed_business_name = models.CharField(max_length=256, blank=True)
    verified_yelp_id = models.CharField(max_length=256, blank=True, default="", unique=True)
    verified = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.business_account == False:
            self.verified = False
            unique_slugify(self, self.verified_yelp_id, slug_field_name='verified_yelp_id')
        super(Profile, self).save(*args, **kwargs)
            
    def __str__(self):
        return f"{self.user.username} Profile"


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    yelp_id = models.CharField(max_length=256)
    business_name = models.CharField(max_length=64, default="StudySpace")
    review_text = models.CharField(max_length=512)
    wifi_rating = models.IntegerField(default=0)
    general_rating = models.IntegerField(default=0)
    food_rating = models.IntegerField(default=0)
    charging_rating = models.IntegerField(default=0)
    comfort_rating = models.IntegerField(default=0)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} \
                reviewed {self.business_name} \
                as {self.review_text} \
                on {self.date_posted}"


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    yelp_id = models.CharField(max_length=256)
    business_name = models.CharField(max_length=64, default="StudySpace")
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.business_name} is {self.user.username}'s favorite"
