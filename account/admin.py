from dataclasses import fields
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from .models import User, Volunter, Squad, VolunterType, SquadType, Admin, Role


class VolunterAdmin(admin.StackedInline):
    model = Volunter
    extra = 0


class SquadAdmin(admin.StackedInline):
    model = Squad
    extra = 0


class AdministratorAdmin(admin.StackedInline):
    model = Admin
    extra = 0


class CustomAddForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "phone")


class UserAdmin(BaseUserAdmin):
    add_form = CustomAddForm
    inlines = [VolunterAdmin, SquadAdmin, AdministratorAdmin]
    ordering = ("email", "role")
    list_display = ("email", "role", "is_active", "is_staff")
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "phone", "password1", "password2"),
            },
        ),
    )
    fieldsets = (
        (
            _("Personal info"),
            {"fields": ("email", "phone", "password", "role", "image")},
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )


admin.site.register(User, UserAdmin)
admin.site.register(Squad)
admin.site.register(Volunter)
admin.site.register(VolunterType)
admin.site.register(SquadType)
admin.site.register(Role)
