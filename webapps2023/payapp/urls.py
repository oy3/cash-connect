from django.urls import path
from .views import dashboard_page, transfer_page, transactions_page, settings_page, help_page, update_profile, get_countries, search_user, create_transaction, accept_fund_request, cancel_fund_request, request_money, search_transactions


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
    path('cancel_fund_request/<int:transaction_id>/', cancel_fund_request, name='cancel_fund_request'),
    # path('accept_fund_request/<int:transaction_id>/', accept_fund_request, name='accept_fund_request'),
    path('accept_fund_request/<int:transaction_id>/<int:sender_id>/<int:receiver_id>/<str:amount_from>/<str:amount_to>/', accept_fund_request, name='accept_fund_request'),
    path('request_money', request_money, name='request_money'),
    path('search_transactions', search_transactions, name='search_transactions'),

]
