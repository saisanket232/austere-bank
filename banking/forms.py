from django import forms
from .models import BankAccount, Beneficiary

class MoneyTransferForm(forms.Form):
    recipient_account = forms.CharField(max_length=20, label='Recipient Account Number')
    amount = forms.DecimalField(max_digits=12, decimal_places=2, min_value=1)
    description = forms.CharField(max_length=255, required=False, label='Remarks')
    otp = forms.CharField(max_length=6, label='OTP (Enter 123456 for demo)')

    def clean_otp(self):
        otp = self.cleaned_data.get('otp')
        if otp != '123456':
            raise forms.ValidationError("Invalid OTP. Use 123456 for demo.")
        return otp

class DepositForm(forms.Form):
    amount = forms.DecimalField(max_digits=12, decimal_places=2, min_value=1)
    description = forms.CharField(max_length=255, required=False, initial='Cash Deposit')

class WithdrawForm(forms.Form):
    amount = forms.DecimalField(max_digits=12, decimal_places=2, min_value=1)
    description = forms.CharField(max_length=255, required=False, initial='Cash Withdrawal')

class BeneficiaryForm(forms.ModelForm):
    class Meta:
        model = Beneficiary
        fields = ['name', 'account_number', 'ifsc_code', 'bank_name']
