from django.contrib import admin
from .models import Fundraising, Transaction


class TransactionAdmin(admin.TabularInline):
    model = Transaction


class FundraisingAdmin(admin.ModelAdmin):
    inlines = [TransactionAdmin]


admin.site.register(Fundraising, FundraisingAdmin)
