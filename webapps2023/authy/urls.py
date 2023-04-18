from django.urls import path
from .views import login_page, login_user, logout_user, change_password
from django.conf.urls import include

app_name = 'authy'
urlpatterns = [
    path('login/', login_page, name='login_page'),
    path('login_user', login_user, name='login_user'),
    path('register', include('register.urls')),
    # path('register_user', register_user, name='register_user'),
    path('logout', logout_user, name='logout_user'),
    path('change_password', change_password, name='change_password'),
]