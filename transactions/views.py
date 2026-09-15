from django.shortcuts import render, get_object_or_404
from .models import Transaction, Account

def transaction_list(request):
    transactions = Transaction.objects.all()
    return render(request, 'transactions/transaction_list.html', {'transactions': transactions})

def transaction_detail(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    return render(request, 'transactions/transaction_detail.html', {'transaction': transaction})

def account_list(request):
    accounts = Account.objects.all()
    return render(request, 'transactions/account_list.html', {'accounts': accounts})
