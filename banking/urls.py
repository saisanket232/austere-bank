from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('transfer/', views.transfer_money, name='transfer'),
    path('transactions/', views.transaction_history, name='transaction_history'),
    path('mini-statement/', views.mini_statement, name='mini_statement'),
    path('deposit/', views.deposit_money, name='deposit'),
    path('withdraw/', views.withdraw_money, name='withdraw'),
    path('beneficiaries/', views.beneficiaries, name='beneficiaries'),
    path('beneficiaries/delete/<int:pk>/', views.delete_beneficiary, name='delete_beneficiary'),
    path('accounts/all/', views.all_accounts, name='all_accounts'),
    path('accounts/toggle/<uuid:pk>/', views.toggle_account, name='toggle_account'),
]
