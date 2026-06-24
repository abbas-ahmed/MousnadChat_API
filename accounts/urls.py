
from django.urls import path
from .view import login_page, logout_page, signup_view , profile , profile_user , upload_file , profile_image ,user_image_load , send_cancel_follow
from . import views
urlpatterns = [
    #path('',   login_page, name="login"),
    #path('logout/', logout_page, name="logout"),
    #path('signup/', signup_view, name="signup"),
    #path('profile/', profile, name="profile"),
    #path('profile_user/', profile_user, name="profile_user"),
    #path('upload_file/', upload_file, name="upload_file") ,
    #path('profile_image/', profile_image, name="profile_image") ,
    #path('user_image_load/', user_image_load, name="user_image_load") ,
    #path('send_cancel_follow/<str:foll>/', send_cancel_follow, name='send_cancel_follow'),

    path('signIn/', views.SignInView, name='signIn'),
    path('register/', views.register, name='register'),
    path('userinfo/', views.current_user, name='user_info'),
    path('userinfo/update/', views.update_user, name='update_user'),
    path('logout_apis_token/', views.logout_apis_token, name='logout_apis_token'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password/<str:token>', views.reset_password, name='reset_password'),
    path('SendCancelFollow/', views.SendCancelFollow, name='SendCancelFollow'),

    path('about_me/', views.update_user_about, name='update_user'),
    path('upload_image/', views.profile_image, name='upload-image'),
    path('user_image/', views.user_image, name='upload-image'),


]
