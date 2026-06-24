from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate

from django.views.decorators.csrf import csrf_exempt


from .models import  UserProfile , Location ,follow_user ,User_image
from .serializers import SingUpSerializer, UserSerializer , UserInfoSerializer


# Create your views here.

def get_auth_for_user(user):
    tokens = RefreshToken.for_user(user)
    userinfo = UserProfile.objects.get(user = user)
    return {
        'user': UserSerializer(user, many=False).data,
        'userinfo':UserInfoSerializer(userinfo, many=False).data ,
        'tokens': {
            'access': str(tokens.access_token),
            'refresh': str(tokens),
        }
    }

@api_view(['POST'])
@permission_classes([AllowAny])
def SignInView(request):

    username = request.data.get('username')
    password = request.data.get('password')
    if not username or not password:
        return Response(status=400)

    user = authenticate(username=username, password=password)

    if not user:
        return Response(status=401)

    user_data = get_auth_for_user(user)

    print(user_data)
    return Response(user_data)



@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    data = request.data
    user = SingUpSerializer(data=data)


    if user.is_valid():
        if not User.objects.filter(username=data['email']).exists():
            user = User.objects.create_user(
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
                username=data['username'],
                password=(data['password']), #make_password(data['password']),
                is_active=True  # تأكد من أن الحساب نشط
            )
            user_pro = UserProfile.objects.create(
                user = user
            )
            return Response(
                {'details': 'Your account registered susccessfully!'},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {'eroor': 'This email already exists!'},
                status=status.HTTP_400_BAD_REQUEST
            )
    else:
        
        return Response(user.errors)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    #user = UserSerializer(request.user, many=False)
    user_ = UserProfile.objects.get(user = request.user)
    uersInfo =UserInfoSerializer( user_ , many=False)
    return Response( uersInfo.data) # user.data ,


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_apis_token(request):
    print(request.data.get("refresh"))
    try:
        refresh_token = request.data.get("refresh")
        token = RefreshToken(refresh_token)
        token.blacklist()

        print("Logout successful")
        return Response(
            {"detail": "Logout successful"},
            status=status.HTTP_205_RESET_CONTENT
        )
    except Exception as e:
        return Response(
            {"detail": "Invalid refresh token"},
            status=status.HTTP_400_BAD_REQUEST
        )



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request):
    user = request.user

    print(user)
    print('///////////////////////////////////////////////////')
    data = request.data
    userInfo = UserProfile.objects.get(user=request.user)
    location_ = Location.objects.get(id=data['location'])
    print(userInfo)

    user.first_name = data['first_name']
    user.last_name = data['last_name']
    user.username = data['username']
    user.last_name = data['last_name']

    #user.email = data['email']

    #if data['password'] != "":
      #  user.password = make_password(data['password'])

    userInfo.about =data['about']
    userInfo.location = location_
    userInfo.date_birthday = data['date_birthday']

    user.save()
    userInfo.save()
    print(data )
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user_about(request):
    user = request.user

    print(user)
    print('///////////////////////////////////////////////////')
    data = request.data
    userInfo = UserProfile.objects.get(user=request.user)
    print(userInfo)
    print(request.data)
    userInfo.about =data['about']

    userInfo.save()
    print(data )
    serializer = UserInfoSerializer(userInfo, many=False)
    print(serializer.data)
    return Response(serializer.data)

def get_current_host(request):
    protocol = request.is_secure() and 'https' or 'http'
    host = request.get_host()
    return "{protocol}://{host}/".format(protocol=protocol, host=host)


@api_view(['POST'])
def forgot_password(request):

    data = request.data
    print(data)
    user = get_object_or_404(User, email=data['email'])
    print()
    token = get_random_string(40)
    expire_date = datetime.now() + timedelta(minutes=30)
    user.profile.reset_password_token = token
    user.profile.reset_password_expire = expire_date
    user.profile.save()

    host = get_current_host(request)
    link = "http://localhost:8000/api/reset_password/{token}".format(token=token)
    body = "Your password reset link is : {link}".format(link=link)
    send_mail(
        "Paswword reset from eMarket",
        body,
        "eMarket@gmail.com",
        [data['email']]
    )
    return Response({'details': 'Password reset sent to {email}'.format(email=data['email'])})


@api_view(['POST'])
def reset_password(request, token):
    data = request.data
    user = get_object_or_404(User, profile__reset_password_token=token)

    if user.profile.reset_password_expire.replace(tzinfo=None) < datetime.now():
        return Response({'error': 'Token is expired'}, status=status.HTTP_400_BAD_REQUEST)

    if data['password'] != data['confirmPassword']:
        return Response({'error': 'Password are not same'}, status=status.HTTP_400_BAD_REQUEST)

    user.password = make_password(data['password'])
    user.profile.reset_password_token = ""
    user.profile.reset_password_expire = None
    user.profile.save()
    user.save()
    return Response({'details': 'Password reset done '})



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def profile_image(request):
    print('*' * 50)
    user_ = UserProfile.objects.get(user =request.user )

    # التحقق من وجود الصورة في الطلب
    if 'image' not in request.FILES:
        return Response(
            {'error': 'No image provided'},
            status=status.HTTP_400_BAD_REQUEST
        )

    image_file = request.FILES['image']

    # التحقق من نوع الملف
    allowed_types = ['image/jpeg', 'image/png', 'image/jpg', 'image/gif']
    if image_file.content_type not in allowed_types:
        return Response(
            {'error': 'Invalid file type. Only images are allowed.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # التحقق من حجم الملف (مثال: 5MB كحد أقصى)
    max_size = 5 * 1024 * 1024  # 5MB
    if image_file.size > max_size:
        return Response(
            {'error': f'File size exceeds {max_size // (1024 * 1024)}MB limit'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # حفظ الصورة
    user_.profile_image = image_file
    user_.save()

    serializer = UserInfoSerializer(user_, many=False)
    print(serializer.data)
    return Response(serializer.data , status=status.HTTP_201_CREATED)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def user_image(request):
    print('*' * 50)
    #user_ = User_image.objects.get(user =request.user )
    user_ , created = User_image.objects.get_or_create(user=request.user)

    # التحقق من وجود الصورة في الطلب
    if 'image' not in request.FILES:
        return Response(
            {'error': 'No image provided'},
            status=status.HTTP_400_BAD_REQUEST
        )

    image_file = request.FILES['image']

    # التحقق من نوع الملف
    allowed_types = ['image/jpeg', 'image/png', 'image/jpg', 'image/gif']
    if image_file.content_type not in allowed_types:
        return Response(
            {'error': 'Invalid file type. Only images are allowed.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # التحقق من حجم الملف (مثال: 5MB كحد أقصى)
    max_size = 5 * 1024 * 1024  # 5MB
    if image_file.size > max_size:
        return Response(
            {'error': f'File size exceeds {max_size // (1024 * 1024)}MB limit'},
            status=status.HTTP_400_BAD_REQUEST
        )

    image_number = int(request.query_params.get('image_number'))
    print(type(image_number))
    # حفظ الصورة
    if image_number == 1 :
        user_.image_one = image_file
        print('#'*50 , image_number)
    elif image_number == 2 :
        user_.image_tow = image_file
        print('#' * 50, image_number)
    elif image_number == 3:
        user_.image_thriy = image_file
        print('#' * 50, image_number)
    elif image_number == 4:
        user_.image_four = image_file
        print('#' * 50, image_number)

    user_.save()

    #serializer = UserInfoSerializer(user_, many=False)
    #print(serializer.data)
    return Response('upload Image seccessfully' ,status=status.HTTP_201_CREATED) #Response(serializer.data , status=status.HTTP_201_CREATED)

