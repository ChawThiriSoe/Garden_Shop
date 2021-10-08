from django.urls import path
from .views import User_Register_View,User_Login_View

app_name = 'users'
urlpatterns =[
    path('register/', User_Register_View, name='user-register'),
    path('login/', User_Login_View, name='user-login')
]