from django.contrib import admin
from .models import Order, Fundraising, Transaction, OrderCategory


class TransactionAdmin(admin.TabularInline):
    model = Transaction


class FundraisingAdmin(admin.ModelAdmin):
    inlines = [TransactionAdmin]


admin.site.register(Order)
admin.site.register(Fundraising, FundraisingAdmin)
admin.site.register(OrderCategory)
