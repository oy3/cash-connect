from django.urls import path
from .views import register_page, register_user

app_name = 'register'
urlpatterns = [
    path('', register_page, name='register_page'),
    path('register_user', register_user, name='register_user')
]
