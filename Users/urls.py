from django.urls import path
from .views import (
    User_Register_View,
    User_Login_View,
    Index_View,
    User_Logout,
    User_Profile,
    User_FgPwd_Email_Accept_View,
    User_Reset_Pwd_View,
    Fruits_View,
    Vegetables_View,
    
    )
from django.conf import settings
from django.conf.urls.static import static


app_name = 'users'
urlpatterns =[
    path('register/', User_Register_View, name='user-register'),
    path('login/', User_Login_View, name='user-login'),
    path('index/',Index_View,name='index'),
    path('logout/',User_Logout,name = 'user-logout'),
    path('<int:id>/profile/',User_Profile,name='user-profile'),
    path('acceptemail/',User_FgPwd_Email_Accept_View,name='user-Fgpwd-EmailAccept'),
    path('resetpwd/',User_Reset_Pwd_View,name='user-reset-pwd'),
    path('fruits/', Fruits_View, name='fruits'),
    path('vegetables/', Vegetables_View, name='vegetables'),

] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)