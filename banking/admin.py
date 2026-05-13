from django.contrib import admin
from .models import BankAccount, Transaction, Beneficiary

@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ['account_number', 'user', 'account_type', 'balance', 'status', 'created_at']
    list_filter = ['account_type', 'status']
    search_fields = ['account_number', 'user__username']

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['reference_number', 'account', 'transaction_type', 'amount', 'created_at']
    list_filter = ['transaction_type']
    search_fields = ['reference_number']

@admin.register(Beneficiary)
class BeneficiaryAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'account_number', 'bank_name']
