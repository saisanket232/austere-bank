from django.contrib import admin
from .models import LoanRequest

@admin.register(LoanRequest)
class LoanRequestAdmin(admin.ModelAdmin):
    list_display = ['user', 'loan_type', 'amount', 'status', 'applied_at']
    list_filter = ['loan_type', 'status']
    search_fields = ['user__username']
