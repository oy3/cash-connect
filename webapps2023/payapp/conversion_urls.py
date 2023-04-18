from django.urls import path
from .views import conversion

app_name = 'conversion'
urlpatterns = [
    path("<str:currency_one>/<str:currency_two>/<str:amount>", conversion, name='conversion'),
]
