from django import forms
from .models import UserProfile
from accounts.models import User_image

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_image']  # "__all__" #['profile_image']
        exclude = ['user']

class UserImageUploadForm(forms.ModelForm):
    class Meta:
        model = User_image
        fields =  "__all__" #['profile_image']
        exclude = ['user']