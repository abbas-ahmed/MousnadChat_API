from rest_framework import serializers
from django.contrib.auth.models import User



from .models import UserProfile, User_image, follow_user, Location


class SingUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','first_name','last_name', 'email', 'password')  #"__all__"

        extra_kwargs = {
            'first_name': {'required':True ,'allow_blank':False},
            'last_name' : {'required':True ,'allow_blank':False},
            'email' : {'required':True ,'allow_blank':False},
            'password' : {'required':True ,'allow_blank':False,'min_length':8}
        }

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','first_name','last_name', 'email', 'username') # "__all__"

#follow_user

class follow_userSerializer(serializers.ModelSerializer):
    sender_follow = UserSerializer()
    receiver_follow = UserSerializer()
    class Meta:
        model = follow_user
        fields = "__all__" # ('sender_follow', 'timestamp', 'is_follow', 'stateName' )


class locationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = "__all__" # ('sender_follow', 'timestamp', 'is_follow', 'stateName' )

class UserImageSerializer(serializers.ModelSerializer):
    #user = UserSerializer()

    class Meta:
        model = User_image
        fields = "__all__" # ('address_one', 'address_two', 'cityName', 'stateName' ,'postCode' ,'user')


class UserInfoSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    location = locationSerializer()

    image_ = serializers.SerializerMethodField()


    class Meta:
        model = UserProfile
        fields = ('id' ,
        'user', 'about',  'profile_image', 'location', 'date_birthday', 'image_',
         )  # "__all__"  # 'followers_', 'following_'

    def get_image_(self, obj):
        # obj هو UserProfile
        # مثال 2: إذا كان هناك علاقة ManyToMany
        image_items = User_image.objects.filter(user=obj.user)
        return UserImageSerializer(image_items, many=True).data





