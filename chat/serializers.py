from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Message
from accounts.models import UserProfile



User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username' ]


class UserInfo_chatSerializer(serializers.ModelSerializer):
    user = UserSerializer()


    class Meta:
        model = UserProfile
        fields = (#
        'user', 'about', 'lang_mother', 'profile_image', 'location', 'date_birthday')  # "__all__
        # "  # , 'fluent_', 'learn_', 'image_','interest_', 'goals_', 'followers_', 'following_'




class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.username', read_only=True)
    receiver_name = serializers.CharField(source='receiver.username', read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'sender_name', 'receiver_name',
                  'content','voice', 'timestamp', 'is_read']