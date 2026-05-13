import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import transaction
from .models import BankAccount, Transaction, Beneficiary
from .forms import MoneyTransferForm, DepositForm, WithdrawForm, BeneficiaryForm
from accounts.models import UserProfile

def role_required(roles):
    from functools import wraps
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            try:
                profile = request.user.profile
                if profile.role not in roles:
                    messages.error(request, 'Access denied.')
                    return redirect('dashboard')
            except UserProfile.DoesNotExist:
                return redirect('login')
            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator

def generate_ref():
    return 'TXN' + str(uuid.uuid4()).replace('-','').upper()[:12]

@login_required
def dashboard(request):
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=request.user, role='customer')
        profile = request.user.profile

    context = {'profile': profile}

    if profile.role == 'admin':
        context['total_users'] = User.objects.count()
        context['total_accounts'] = BankAccount.objects.count()
        context['total_balance'] = sum(a.balance for a in BankAccount.objects.all())
        context['recent_txns'] = Transaction.objects.all()[:10]
        context['all_accounts'] = BankAccount.objects.select_related('user').all()[:10]
        from loans.models import LoanRequest
        context['pending_loans'] = LoanRequest.objects.filter(status='pending').count()
        context['total_loans'] = LoanRequest.objects.count()

    elif profile.role == 'employee':
        context['total_accounts'] = BankAccount.objects.count()
        context['recent_txns'] = Transaction.objects.all()[:10]
        from loans.models import LoanRequest
        context['pending_loans'] = LoanRequest.objects.filter(status='pending')

    else:  # customer
        accounts = BankAccount.objects.filter(user=request.user)
        context['accounts'] = accounts
        if accounts.exists():
            context['account'] = accounts.first()
            context['recent_txns'] = accounts.first().transactions.all()[:5]
        from loans.models import LoanRequest
        context['my_loans'] = LoanRequest.objects.filter(user=request.user)

    return render(request, 'banking/dashboard.html', context)

@login_required
def transfer_money(request):
    account = get_object_or_404(BankAccount, user=request.user, status='active')
    if request.method == 'POST':
        form = MoneyTransferForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            recipient_acc_num = form.cleaned_data['recipient_account']
            desc = form.cleaned_data['description'] or 'Fund Transfer'

            if amount > account.balance:
                messages.error(request, 'Insufficient balance.')
            elif recipient_acc_num == account.account_number:
                messages.error(request, 'Cannot transfer to your own account.')
            else:
                try:
                    recipient_account = BankAccount.objects.get(account_number=recipient_acc_num)
                    if recipient_account.status != 'active':
                        messages.error(request, 'Recipient account is frozen or inactive.')
                    else:
                        with transaction.atomic():
                            # Debit sender
                            account.balance -= amount
                            account.save()
                            ref = generate_ref()
                            Transaction.objects.create(
                                account=account,
                                transaction_type='debit',
                                amount=amount,
                                balance_after=account.balance,
                                description=f'Transfer to {recipient_acc_num} - {desc}',
                                reference_number=ref,
                                recipient_account=recipient_acc_num
                            )
                            # Credit receiver
                            recipient_account.balance += amount
                            recipient_account.save()
                            Transaction.objects.create(
                                account=recipient_account,
                                transaction_type='credit',
                                amount=amount,
                                balance_after=recipient_account.balance,
                                description=f'Transfer from {account.account_number} - {desc}',
                                reference_number='RCV'+ref[3:],
                                recipient_account=account.account_number
                            )
                    messages.success(request, f'₹{amount} transferred successfully! Ref: {ref}')
                    return redirect('transaction_history')
                except BankAccount.DoesNotExist:
                    messages.error(request, 'Recipient account not found.')
    else:
        form = MoneyTransferForm()
    return render(request, 'banking/transfer.html', {'form': form, 'account': account})

@login_required
def transaction_history(request):
    accounts = BankAccount.objects.filter(user=request.user)
    if not accounts.exists():
        return render(request, 'banking/transactions.html', {'error': 'No account found.'})
    
    account = accounts.first()
    txns = account.transactions.all()
    # Filter
    filter_type = request.GET.get('type', '')
    if filter_type:
        txns = txns.filter(transaction_type=filter_type)
    return render(request, 'banking/transactions.html', {
        'account': account, 'transactions': txns, 'filter_type': filter_type
    })

@login_required
def mini_statement(request):
    account = BankAccount.objects.filter(user=request.user).first()
    if not account:
        return redirect('dashboard')
    txns = account.transactions.all()[:10]
    return render(request, 'banking/mini_statement.html', {'account': account, 'transactions': txns})

@login_required
@role_required(['admin', 'employee'])
def deposit_money(request):
    if request.method == 'POST':
        form = DepositForm(request.POST)
        acc_num = request.POST.get('account_number')
        if form.is_valid():
            try:
                account = BankAccount.objects.get(account_number=acc_num)
                if account.status != 'active':
                    messages.error(request, f'Account {acc_num} is {account.status} and cannot receive deposits.')
                    return redirect('deposit')
                amount = form.cleaned_data['amount']
                desc = form.cleaned_data['description'] or 'Cash Deposit'
                with transaction.atomic():
                    account.balance += amount
                    account.save()
                    Transaction.objects.create(
                        account=account,
                        transaction_type='credit',
                        amount=amount,
                        balance_after=account.balance,
                        description=desc,
                        reference_number=generate_ref()
                    )
                messages.success(request, f'₹{amount} deposited to {acc_num}.')
                return redirect('dashboard')
            except BankAccount.DoesNotExist:
                messages.error(request, 'Account not found.')
    else:
        form = DepositForm()
    return render(request, 'banking/deposit.html', {'form': form})

@login_required
@role_required(['admin', 'employee'])
def withdraw_money(request):
    if request.method == 'POST':
        form = WithdrawForm(request.POST)
        acc_num = request.POST.get('account_number')
        if form.is_valid():
            try:
                account = BankAccount.objects.get(account_number=acc_num)
                if account.status != 'active':
                    messages.error(request, f'Account {acc_num} is {account.status} and cannot perform withdrawals.')
                    return redirect('withdraw')
                amount = form.cleaned_data['amount']
                desc = form.cleaned_data['description'] or 'Cash Withdrawal'
                
                if account.balance < amount:
                    messages.error(request, 'Insufficient balance in customer account.')
                else:
                    with transaction.atomic():
                        account.balance -= amount
                        account.save()
                        Transaction.objects.create(
                            account=account,
                            transaction_type='debit',
                            amount=amount,
                            balance_after=account.balance,
                            description=desc,
                            reference_number=generate_ref()
                        )
                    messages.success(request, f'₹{amount} withdrawn from {acc_num}.')
                    return redirect('dashboard')
            except BankAccount.DoesNotExist:
                messages.error(request, 'Account not found.')
    else:
        form = WithdrawForm()
    return render(request, 'banking/withdraw.html', {'form': form})

@login_required
def beneficiaries(request):
    bens = Beneficiary.objects.filter(user=request.user)
    form = BeneficiaryForm()
    if request.method == 'POST':
        form = BeneficiaryForm(request.POST)
        if form.is_valid():
            b = form.save(commit=False)
            b.user = request.user
            b.save()
            messages.success(request, 'Beneficiary added.')
            return redirect('beneficiaries')
    return render(request, 'banking/beneficiaries.html', {'beneficiaries': bens, 'form': form})

@login_required
def delete_beneficiary(request, pk):
    b = get_object_or_404(Beneficiary, pk=pk, user=request.user)
    b.delete()
    messages.success(request, 'Beneficiary removed.')
    return redirect('beneficiaries')

@login_required
@role_required(['admin', 'employee'])
def all_accounts(request):
    accounts = BankAccount.objects.select_related('user').all()
    return render(request, 'banking/all_accounts.html', {'accounts': accounts})

@login_required
@role_required(['admin', 'employee'])
def toggle_account(request, pk):
    account = get_object_or_404(BankAccount, pk=pk)
    if account.status == 'active':
        account.status = 'frozen'
        messages.warning(request, f'Account {account.account_number} frozen.')
    else:
        account.status = 'active'
        messages.success(request, f'Account {account.account_number} activated.')
    account.save()
    return redirect('all_accounts')
