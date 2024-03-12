from django import forms
from django.utils.translation import gettext_lazy as _
from .models import User, Volunter, Squad
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class UserCreate(UserCreationForm):
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
