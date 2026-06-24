from os import name

from django.urls import path
from . import views



urlpatterns =[
  
  #path('', views.index , name="index"),
  path('', views.index, name="index"),
  path('home/', views.home , name="home"),
  #path('about',views.about,name="about"),
  #path('More',views.More,name="More"),
  #path('Setting',views.Setting,name="Setting"),


]