import os

from django.db import models
from django.contrib.auth.models import User
# Create your models here.



def user_image_path(instance ,filename):
    # سيعيد: static/image/username/filename
    return os.path.join('static', 'image', f'{instance.user.username}_{instance.user.id}', filename)



class Location(models.Model):
    name_country = models.CharField(max_length=150, unique=True )
    icon_country = models.CharField(  max_length=1000 )
    is_enabled = models.BooleanField(default=True)


    def __str__(self):
        return f"{self.name_country} "


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.TextField(blank=True, null=True)
    #lang_mother = models.ForeignKey(Langs , on_delete=models.SET_NULL, null=True, blank=True)
    profile_image = models.ImageField(
        upload_to= user_image_path ,#'static/image/',  blank=True , null=True,
        default='static/image/default.jpg'
    ) # 'photos/%Y/%m/%d'
    location = models.ForeignKey(
        Location, on_delete=models.SET_NULL,  null=True, blank=True
    )
    date_birthday = models.DateField(null=True, blank=True , default="1993-10-10")
    date_joined = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.user.username}'s Profile"



class User_image (models.Model)   :
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image_one= models.ImageField(
        upload_to=user_image_path,
        #blank=True,
        #null=True,
        default='static/image/default.jpg'
    )  # 'photos/%Y/%m/%d'
    image_tow = models.ImageField(
        upload_to=user_image_path,
        #blank=True,
       # null=True,
        default='static/image/default.jpg'
    )
    image_thriy = models.ImageField(
        upload_to=user_image_path,
       # blank=True,
        #null=True,
        default='static/image/default.jpg'
    )
    image_four = models.ImageField(
        upload_to=user_image_path,
        #blank=True,
        #null=True,
        default='static/image/default.jpg'
    )


class follow_user (models.Model):
    sender_follow = models.ForeignKey(User, related_name="sent_follow", on_delete=models.CASCADE)
    receiver_follow = models.ForeignKey(User, related_name="received_follow", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_follow = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.sender_follow.username} -> {self.receiver_follow.username}: {self.is_follow}"