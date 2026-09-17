from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from .models import Transaction, Account
#
# def transaction_list(request):
#     transactions = Transaction.objects.all()
#     return render(request, 'transaction_list.html', {'transactions': transactions})
#
# def transaction_detail(request, pk):
#     transaction = get_object_or_404(Transaction, pk=pk)
#     return render(request, 'transactions/transaction_detail.html', {'transaction': transaction})
#
# def account_list(request):
#     accounts = Account.objects.all()
#     return render(request, 'transactions/account_list.html', {'accounts': accounts})

class TransactionListView(ListView):
    model = Transaction
    template_name = 'transactions/transaction_list.html'
    context_object_name = 'transactions'
    ordering = ['-created_at']
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(comment_icontains=query)
        return queryset


class LargeExpensesListView(ListView):
     model = Transaction
     template_name = 'transactions/large_expenses.html'
     context_object_name = 'transactions'
     ordering = ['-amount']
     paginate_by = 5

     def get_queryset(self):
         return Transaction.objects.filter(transaction_type='expense', amount__gt=500.00)


class TransactionDetailView(DetailView):
    model = Transaction
    template_name = 'transactions/transaction_detail.html'
    context_object_name = 'transaction'


class AccountListView(ListView):
    model = Account
    template_name = 'transactions/account_list.html'
    context_object_name = 'accounts'


class AccountDetailView(DetailView):
    model = Account
    template_name = 'transactions/account_detail.html'
    context_object_name = 'account'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['account_transactions'] = Transaction.objects.filter(account=self.object)
        return context


class TransactionCreateView(SuccessMessageMixin, CreateView):
    model = Transaction
    fields = ['account', 'category', 'tags', 'amount', 'transaction_type', 'created_at', 'comment']
    template_name = 'transactions/transaction_form.html'
    success_message = 'Transaction was successfully recorded in the ledger!'


class TransactionUpdateView(SuccessMessageMixin, UpdateView):
    model = Transaction
    fields = ['account', 'category', 'tags', 'amount', 'transaction_type', 'created_at', 'comment']
    template_name = 'transactions/transaction_form.html'


class TransactionDeleteView(DeleteView):
    model = Transaction
    template_name = 'transactions/transaction_confirm_delete.html'
    success_url = reverse_lazy('transaction_list')


class AccountCreateView(CreateView):
    model = Account
    fields = ['name', 'account_type', 'balance']
    template_name = 'transactions/account_form.html'


class AccountUpdateView(UpdateView):
    model = Account
    fields = ['name', 'account_type', 'balance']
    template_name = 'transactions/account_form.html'