import uuid
from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

LOAN_TYPES = [
    ('personal', 'Personal Loan'),
    ('home', 'Home Loan'),
    ('car', 'Car Loan'),
    ('education', 'Education Loan'),
    ('business', 'Business Loan'),
]

LOAN_STATUS = [
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
    ('disbursed', 'Disbursed'),
    ('closed', 'Closed'),
]

INTEREST_RATES = {
    'personal': Decimal('12.5'),
    'home': Decimal('8.5'),
    'car': Decimal('10.0'),
    'education': Decimal('9.0'),
    'business': Decimal('14.0'),
}

class LoanRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loan_requests')
    loan_type = models.CharField(max_length=20, choices=LOAN_TYPES)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    tenure_months = models.IntegerField()
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=10.0)
    emi_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    purpose = models.TextField()
    status = models.CharField(max_length=20, choices=LOAN_STATUS, default='pending')
    reviewed_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_loans'
    )
    review_note = models.TextField(blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.loan_type} - ₹{self.amount}"

    def calculate_emi(self):
        P = float(self.amount)
        r = float(self.interest_rate) / (12 * 100)
        n = self.tenure_months
        if r == 0:
            return P / n
        emi = P * r * (1 + r)**n / ((1 + r)**n - 1)
        return round(emi, 2)

    def total_payable(self):
        return round(self.calculate_emi() * self.tenure_months, 2)

    def total_interest(self):
        return round(self.total_payable() - float(self.amount), 2)

    def save(self, *args, **kwargs):
        if not self.interest_rate or self.interest_rate == 10:
            self.interest_rate = INTEREST_RATES.get(self.loan_type, Decimal('10.0'))
        self.emi_amount = Decimal(str(self.calculate_emi()))
        super().save(*args, **kwargs)
