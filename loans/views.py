from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from decimal import Decimal
from .models import LoanRequest, INTEREST_RATES
from .forms import LoanApplicationForm, LoanReviewForm, EMICalculatorForm
from accounts.models import UserProfile

def role_required(roles):
    from functools import wraps
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            try:
                if request.user.profile.role not in roles:
                    messages.error(request, 'Access denied.')
                    return redirect('dashboard')
            except UserProfile.DoesNotExist:
                return redirect('login')
            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator

@login_required
def apply_loan(request):
    if request.method == 'POST':
        form = LoanApplicationForm(request.POST)
        if form.is_valid():
            loan = form.save(commit=False)
            loan.user = request.user
            loan.save()
            messages.success(request, f'Loan application submitted! Your application ID: {str(loan.id)[:8].upper()}')
            return redirect('my_loans')
    else:
        form = LoanApplicationForm()
    return render(request, 'loans/apply.html', {'form': form, 'rates': INTEREST_RATES})

@login_required
def my_loans(request):
    loans = LoanRequest.objects.filter(user=request.user)
    return render(request, 'loans/my_loans.html', {'loans': loans})

@login_required
def loan_detail(request, pk):
    loan = get_object_or_404(LoanRequest, pk=pk, user=request.user)
    return render(request, 'loans/loan_detail.html', {'loan': loan})

@login_required
@role_required(['admin', 'employee'])
def all_loans(request):
    status_filter = request.GET.get('status', '')
    loans = LoanRequest.objects.select_related('user').all()
    if status_filter:
        loans = loans.filter(status=status_filter)
    return render(request, 'loans/all_loans.html', {'loans': loans, 'status_filter': status_filter})

@login_required
@role_required(['admin', 'employee'])
def review_loan(request, pk):
    loan = get_object_or_404(LoanRequest, pk=pk)
    if request.method == 'POST':
        form = LoanReviewForm(request.POST, instance=loan)
        if form.is_valid():
            reviewed = form.save(commit=False)
            reviewed.reviewed_by = request.user
            reviewed.save()
            # If approved, disburse to account
            if reviewed.status == 'disbursed':
                from banking.models import BankAccount, Transaction
                import uuid
                try:
                    account = BankAccount.objects.get(user=loan.user, status='active')
                    account.balance += loan.amount
                    account.save()
                    Transaction.objects.create(
                        account=account,
                        transaction_type='credit',
                        amount=loan.amount,
                        balance_after=account.balance,
                        description=f'{loan.get_loan_type_display()} Loan Disbursement',
                        reference_number='LDN' + str(uuid.uuid4()).replace('-','').upper()[:10]
                    )
                    messages.success(request, f'Loan disbursed and ₹{loan.amount} credited to customer account.')
                except BankAccount.DoesNotExist:
                    messages.warning(request, 'Loan approved but customer has no active account.')
            else:
                messages.success(request, f'Loan status updated to {reviewed.status}.')
            return redirect('all_loans')
    else:
        form = LoanReviewForm(instance=loan)
    return render(request, 'loans/review_loan.html', {'form': form, 'loan': loan})

def emi_calculator(request):
    result = None
    if request.method == 'POST':
        form = EMICalculatorForm(request.POST)
        if form.is_valid():
            P = float(form.cleaned_data['principal'])
            n = form.cleaned_data['tenure_months']
            loan_type = form.cleaned_data['loan_type']
            custom_rate = form.cleaned_data.get('interest_rate')
            annual_rate = float(custom_rate) if custom_rate else float(INTEREST_RATES.get(loan_type, 10))
            r = annual_rate / (12 * 100)
            if r == 0:
                emi = P / n
            else:
                emi = P * r * (1+r)**n / ((1+r)**n - 1)
            total = emi * n
            result = {
                'emi': round(emi, 2),
                'total': round(total, 2),
                'interest': round(total - P, 2),
                'principal': P,
                'rate': annual_rate,
                'tenure': n,
            }
    else:
        form = EMICalculatorForm()
    return render(request, 'loans/emi_calculator.html', {'form': form, 'result': result})

# Override loan_detail to pass formatted data
from django.shortcuts import render as _render
_orig_loan_detail = loan_detail
def loan_detail(request, pk):
    loan = get_object_or_404(LoanRequest, pk=pk, user=request.user)
    details = [
        ('Principal', f'₹{loan.amount}', 'var(--gold)'),
        ('Monthly EMI', f'₹{loan.emi_amount}', '#4ade80'),
        ('Total Payable', f'₹{loan.total_payable}', 'var(--white)'),
        ('Total Interest', f'₹{loan.total_interest}', '#f87171'),
        ('Interest Rate', f'{loan.interest_rate}% p.a.', 'var(--silver)'),
        ('Tenure', f'{loan.tenure_months} months', 'var(--silver)'),
    ]
    info = [
        ('Loan Type', loan.get_loan_type_display()),
        ('Status', loan.status.capitalize()),
        ('Purpose', loan.purpose),
        ('Applied On', loan.applied_at.strftime('%d %b %Y %H:%M')),
    ]
    if loan.reviewed_by:
        info.append(('Reviewed By', loan.reviewed_by.get_full_name()))
    if loan.review_note:
        info.append(('Bank Note', loan.review_note))
    return _render(request, 'loans/loan_detail.html', {'loan': loan, 'details': details, 'info': info})

_orig_review = review_loan
def review_loan(request, pk):
    loan = get_object_or_404(LoanRequest, pk=pk)
    info_rows = [
        ('Customer', loan.user.get_full_name()),
        ('Email', loan.user.email),
        ('Loan Type', loan.get_loan_type_display()),
        ('Amount', f'₹{loan.amount}'),
        ('Tenure', f'{loan.tenure_months} months'),
        ('Interest Rate', f'{loan.interest_rate}% p.a.'),
        ('Purpose', loan.purpose),
        ('Applied On', loan.applied_at.strftime('%d %b %Y %H:%M')),
        ('Current Status', loan.status.capitalize()),
    ]
    if request.method == 'POST':
        form = LoanReviewForm(request.POST, instance=loan)
        if form.is_valid():
            reviewed = form.save(commit=False)
            reviewed.reviewed_by = request.user
            reviewed.save()
            if reviewed.status == 'disbursed':
                from banking.models import BankAccount, Transaction
                import uuid
                try:
                    account = BankAccount.objects.get(user=loan.user, status='active')
                    account.balance += loan.amount
                    account.save()
                    Transaction.objects.create(
                        account=account, transaction_type='credit',
                        amount=loan.amount, balance_after=account.balance,
                        description=f'{loan.get_loan_type_display()} Loan Disbursement',
                        reference_number='LDN'+str(uuid.uuid4()).replace('-','').upper()[:10]
                    )
                    messages.success(request, f'Loan disbursed. ₹{loan.amount} credited to customer.')
                except BankAccount.DoesNotExist:
                    messages.warning(request, 'Loan approved but customer has no active account.')
            else:
                messages.success(request, f'Loan status updated to {reviewed.status}.')
            return redirect('all_loans')
    else:
        form = LoanReviewForm(instance=loan)
    return _render(request, 'loans/review_loan.html', {'form': form, 'loan': loan, 'info_rows': info_rows})
