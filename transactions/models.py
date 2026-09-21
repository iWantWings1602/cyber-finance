from django.db import models
from django.core.validators import MinValueValidator
from django.urls import reverse
from django.contrib.auth.models import User


class Account(models.Model):
    ACCOUNT_TYPES = [
        ('cash', 'Cash'),
        ('card', 'Bank Card'),
        ('crypto', 'Crypto Wallet'),
        ('deposit', 'Deposit'),
    ]

    name = models.CharField(max_length=50, verbose_name='Account Name')
    account_type = models.CharField(
        max_length=10,
        choices=ACCOUNT_TYPES,
        default='card',
        verbose_name='Account type'
    )
    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        verbose_name='Current Balance'
    )

    def __str__(self):
        return f'{self.name} ({self.get_account_type_display()}) - {self.balance} UAH'

    @property
    def is_negative(self):
        return self.balance < 0

    def get_absolute_url(self):
        return reverse('account_list')

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Category Name')
    is_expense = models.BooleanField(default=False, verbose_name='Is Expense?')

    def __str__(self):
        type_str = 'Expense' if self.is_expense else 'Income'
        return f'{self.name} ({type_str})'

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name='Tag Name')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('expense', 'Expense'),
        ('income', 'Income'),
    ]

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='transactions',
        null=True,
        verbose_name='Owner')

    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        verbose_name='Account')

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='transactions',
        verbose_name='Category'
    )

    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='transactions',
        verbose_name='Tags'
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        verbose_name='Amount'
    )

    transaction_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_TYPES,
        verbose_name='Transaction Type'
    )

    created_at = models.DateTimeField(verbose_name='Date and Time')
    comment = models.TextField(blank=True, verbose_name='Comment')

    def __str__(self):
        sign = '-' if self.transaction_type == 'expense' else '+'
        return f'{self.created_at.strftime('%d.%m.%Y')} : {sign}{self.amount} UAH ({self.account.name})'

    def get_absolute_url(self):
        return reverse('transaction_detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
        ordering = ['-created_at']
