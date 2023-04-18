from django.urls import path
from .views import dashboard_page, transfer_page, transactions_page, settings_page

app_name = 'dashboard'
urlpatterns = [
    path('', dashboard_page, name='dashboard_page'),
    path('transfer', transfer_page, name='transfer_page'),
    path('transactions', transactions_page, name='transactions_page'),
    path('settings', settings_page, name='settings_page')
]
