from django.urls import path
from .views import dashboard_page, transfer_page, transactions_page, settings_page, help_page, update_profile, get_countries, search_user, create_transaction, request_money


app_name = 'payapp'
urlpatterns = [
    path('', dashboard_page, name='dashboard_page'),
    path('transfer', transfer_page, name='transfer_page'),
    path('transactions', transactions_page, name='transactions_page'),
    path('settings', settings_page, name='settings_page'),
    path('help', help_page, name='help_page'),
    path('update_profile', update_profile, name='update_profile'),
    path('get_countries', get_countries, name='get_countries'),
    path('search_user', search_user, name='search_user'),
    path('create_transaction', create_transaction, name='create_transaction'),
    path('request_money', request_money, name='request_money'),
]
