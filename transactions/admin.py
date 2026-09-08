from django.contrib import admin
from .models import Account, Category, Tag, Transaction

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'account_type', 'balance', 'is_negative')
    list_filter = ('account_type',)
    search_fields = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_expense')
    list_filter = ('is_expense',)
    search_fields = ('name',)

    actions = ['make_income']

    @admin.action(description='Convert selected categories to Income')
    def make_income(self, request, queryset):
        updated = queryset.update(is_expense=False)
        self.message_user(request, f'Successfully updated {updated} categories.')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'account', 'category', 'transaction_type', 'amount')
    list_filter = ('transaction_type', 'account', 'category', 'created_at')
    search_fields = ('comment', 'account__name', 'category__name')
    filter_horizontal = ('tags',)
