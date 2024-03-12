from django import forms
from django.utils.translation import gettext_lazy as _
from .models import User, Volunter, Squad, Role
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class UserCreate(UserCreationForm):
    def __init__(self, *args, **kwargs):
        qs = Role.objects.filter(is_active=True)
        super(UserCreate, self).__init__(*args, **kwargs)
        self.fields["role"].queryset = qs

    class Meta:
        model = User
        fields = ["email", "phone", "role", "password1", "password2"]


class UserChange(UserChangeForm):
    class Meta:
        model = User
        fields = ["image", "email", "phone", "password"]


class VolunterCreate(forms.ModelForm):
    class Meta:
        model = Volunter
        exclude = ["user"]


class VolunterChange(forms.ModelForm):
    class Meta:
        model = Volunter
        exclude = ["user"]


class SquadCreate(forms.ModelForm):
    class Meta:
        model = Squad
        exclude = ["user"]


class SquadChange(forms.ModelForm):
    class Meta:
        model = Squad
        exclude = ["user"]
