from django import forms
from .models import LoanRequest, LOAN_TYPES

class LoanApplicationForm(forms.ModelForm):
    tenure_months = forms.ChoiceField(choices=[
        (6,'6 Months'),(12,'12 Months'),(24,'24 Months'),
        (36,'36 Months'),(48,'48 Months'),(60,'60 Months'),
        (84,'84 Months'),(120,'10 Years'),(180,'15 Years'),(240,'20 Years'),
    ])

    class Meta:
        model = LoanRequest
        fields = ['loan_type', 'amount', 'tenure_months', 'purpose']
        widgets = {'purpose': forms.Textarea(attrs={'rows': 3})}

class LoanReviewForm(forms.ModelForm):
    class Meta:
        model = LoanRequest
        fields = ['status', 'review_note']
        widgets = {'review_note': forms.Textarea(attrs={'rows': 3})}

class EMICalculatorForm(forms.Form):
    loan_type = forms.ChoiceField(choices=LOAN_TYPES)
    principal = forms.DecimalField(max_digits=12, decimal_places=2, min_value=1000, label='Loan Amount (₹)')
    tenure_months = forms.IntegerField(min_value=1, max_value=360, label='Tenure (Months)')
    interest_rate = forms.DecimalField(max_digits=5, decimal_places=2, required=False, label='Custom Rate % (optional)')
