from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path('signup/',views.createUser,name='createUser'),
    path('login/',obtain_auth_token,name='login'),
    path('logout/',views.logout,name='logout')
]