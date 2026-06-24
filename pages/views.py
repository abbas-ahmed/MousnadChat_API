from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
#from products.models import Product
from django.contrib.auth.models import User, Group
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response




@api_view(['GET'])
@permission_classes([AllowAny])
def index(request):
    print('you are in index app Musnad')

    return Response({
                        'uersInfo_community':'You are in index page in  app Musnad',
                    })


@login_required
def home(request):


    user_community = User.objects.exclude(id=request.user.id)

    # Sort user_last_messages by the timestamp of the last_message in descending order

    content = {
        user_community: 'user_community'
    }

    #print(user_community)
    #products_all = Product.objects.all()
    #conten = {'products_all':products_all,}
    return render (request ,'Community/Community.html' , context=content) # pages/index_.html

def about (request):
    return render(request ,'pages/about.html')




def More(request):
    return render(request , 'pages/More.html')

def Setting(request):
    return render(request , 'pages/Setting.html')
