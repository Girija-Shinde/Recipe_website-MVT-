from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register_page, name='register'),
    path('login/', login_page, name='login'),
    path('logout/', logout_page, name='logout'),
    path('my_profile/',my_profile, name ='my_profile'),
    path('edit_profile/', edit_profile, name = 'edit_profile'),
    path('change_password/', change_password, name='change_password'),
]
