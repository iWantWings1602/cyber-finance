from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Transaction, Account
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin


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

#   Registration + Auto-login
class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('transaction_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response

        # LISTS AND DETAILS
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


class MyTransactionsListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'transactions/transaction_list.html'
    context_object_name = 'transactions'
    ordering = ['-created_at']
    paginate_by = 5

    def get_queryset(self):
        return Transaction.objects.filter(owner=self.request.user)


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


class TransactionCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Transaction
    fields = ['account', 'category', 'tags', 'amount', 'transaction_type', 'created_at', 'comment']
    template_name = 'transactions/transaction_form.html'
    success_message = 'Transaction recorded successfully!'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class TransactionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Transaction
    fields = ['account', 'category', 'tags', 'amount', 'transaction_type', 'created_at', 'comment']
    template_name = 'transactions/transaction_form.html'

    def test_func(self):
        obj = self.get_object()
        return obj.owner == self.request.user or self.request.user.is_staff


class TransactionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Transaction
    template_name = 'transactions/transaction_confirm_delete.html'
    success_url = reverse_lazy('transaction_list')

    def test_func(self):
        obj = self.get_object()
        return obj.owner == self.request.user or self.request.user.is_staff

# ACCOUNTS
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


class AccountCreateView(CreateView):
    model = Account
    fields = ['name', 'account_type', 'balance']
    template_name = 'transactions/account_form.html'


class AccountUpdateView(UpdateView):
    model = Account
    fields = ['name', 'account_type', 'balance']
    template_name = 'transactions/account_form.html'