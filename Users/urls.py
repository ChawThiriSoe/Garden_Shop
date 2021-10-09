from django.urls import path
from .views import User_Register_View,User_Login_View,Index_View,User_Logout
from django.conf import settings
from django.conf.urls.static import static

app_name = 'users'
urlpatterns =[
    path('register/', User_Register_View, name='user-register'),
    path('login/', User_Login_View, name='user-login'),
    path('index/',Index_View,name='index'),
    path('logout/',User_Logout,name = 'user-logout'),

]+ static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)