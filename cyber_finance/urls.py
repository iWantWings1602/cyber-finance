"""
URL configuration for cyber_finance project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from transactions import views


urlpatterns = [
    path('admin/', admin.site.urls),
        #Вбудовані маршрути для login та logout
    path('accounts/', include('django.contrib.auth.urls')),
        #Кастомний маршрут для реєстрації (signup)
    path('accounts/signup/', views.SignUpView.as_view(), name='signup'),
        #Маршрути для нашого застосунку
    path('', views.TransactionListView.as_view(), name='transaction_list'),
    path('transactions/new/', views.TransactionCreateView.as_view(), name='transaction_create'),
    path('transactions/my/', views.MyTransactionsListView.as_view(), name='my_transactions'),
    path('transactions/large/', views.LargeExpensesListView.as_view(), name='large_expenses'),
    path('transactions/<int:pk>/', views.TransactionDetailView.as_view(), name='transaction_detail'),
    path('transactions/<int:pk>/edit/', views.TransactionUpdateView.as_view(), name='transaction_update'),
    path('transactions/<int:pk>/delete/', views.TransactionDeleteView.as_view(), name='transaction_delete'),
        #Маршрути для рахунків
    path('accounts_list/', views.AccountListView.as_view(), name='account_list'),
    path('accounts_list/new/', views.AccountCreateView.as_view(), name='account_create'),
    path('accounts_list/<int:pk>/', views.AccountDetailView.as_view(), name='account_detail'),
    path('accounts_list/<int:pk>/edit/', views.AccountUpdateView.as_view(), name='account_update'),
]

