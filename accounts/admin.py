from django.contrib import admin
from .models import Location, UserProfile ,User_image , follow_user


# Register your models here.

admin.site.register(Location)
admin.site.register(UserProfile)
admin.site.register(User_image)
admin.site.register(follow_user)
