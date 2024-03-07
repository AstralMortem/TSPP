from django import forms
from django.utils.translation import gettext_lazy as _
from .models import User, Volunter, Squad
from django.contrib.auth.forms import UserCreationForm


class UserCreate(UserCreationForm):
    class Meta:
        model = User
        fields = ["email", "phone", "role", "password1", "password2"]


class VolunterCreate(forms.ModelForm):
    class Meta:
        model = Volunter
        exclude = ["user"]


class SquadCreate(forms.ModelForm):
    class Meta:
        model = Squad
        exclude = ["user"]
