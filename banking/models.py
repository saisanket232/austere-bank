import uuid
from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

ACCOUNT_TYPES = [
    ('savings', 'Savings'),
    ('current', 'Current'),
    ('fixed', 'Fixed Deposit'),
]

TRANSACTION_TYPES = [
    ('credit', 'Credit'),
    ('debit', 'Debit'),
    ('transfer', 'Transfer'),
]

STATUS_CHOICES = [
    ('active', 'Active'),
    ('inactive', 'Inactive'),
    ('frozen', 'Frozen'),
]

class BankAccount(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bank_accounts')
    account_number = models.CharField(max_length=20, unique=True)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES, default='savings')
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    ifsc_code = models.CharField(max_length=15, default='AUSR0001001')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.account_number} - {self.user.username}"

    def get_masked_number(self):
        return f"XXXX XXXX {self.account_number[-4:]}"

class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    balance_after = models.DecimalField(max_digits=15, decimal_places=2)
    description = models.CharField(max_length=255, blank=True)
    reference_number = models.CharField(max_length=30, unique=True)
    recipient_account = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.reference_number} - {self.transaction_type} - ₹{self.amount}"

class Beneficiary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='beneficiaries')
    name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=20)
    ifsc_code = models.CharField(max_length=15)
    bank_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.account_number}"

    class Meta:
        verbose_name_plural = "Beneficiaries"
