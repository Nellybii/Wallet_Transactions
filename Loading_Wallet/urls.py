from django.urls import path
from .views import load_wallet_views

urlpatterns = [
    path('load_wallet/', load_wallet_views.load_wallet_view, name='load_wallet'),
    path('transactions/', load_wallet_views.get_all_transactions, name='get_all_transactions'),
    path('mpesa/validation', load_wallet_views.mpesa_validation, name='mpesa_validation'),
    path('mpesa/confirmation', load_wallet_views.mpesa_confirmation, name='mpesa_confirmation'),
]
