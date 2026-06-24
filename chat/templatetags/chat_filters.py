# myapp/templatetags/user_filters.py

from django import template
from accounts.models import *
from datetime import date

register = template.Library()

@register.filter
def return_image_user_( id_user ):

    profile_img = UserProfile.objects.get(user=id_user)
    image_value = profile_img.profile_image.url
    if not image_value :
        image_value = "static/image/default.jpg"

    return image_value



