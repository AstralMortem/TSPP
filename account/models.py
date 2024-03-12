from email.policy import default
from enum import unique
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.utils.translation import gettext_lazy as _
from django.contrib.staticfiles import finders
from channels.db import database_sync_to_async


# Base auth manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, phone, password=None, **extra_fields):
        if not email:
            raise ValueError(_("Email should be set"))
        if not phone:
            raise ValueError(_("Phone should be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        user = self.create_user(email, phone, password, **extra_fields)
        # Create admin profile with full_name = phone
        # but manager still return Base user model
        Admin.objects.create(user=user, full_name=phone)
        return user


class Role(models.Model):
    title = models.CharField(_("title"), max_length=254)
    is_active = models.BooleanField(_("Is active role"), default=True)

    def __str__(self):
        return self.title


# Base user class
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("Email"), max_length=254, unique=True)
    phone = models.CharField(_("Phone"), max_length=13)
    image = models.ImageField(
        _("Image"), upload_to="users/avatars", null=True, blank=True
    )
    role = models.ForeignKey(Role, on_delete=models.PROTECT, blank=True, null=True)
    is_active = models.BooleanField(_("Is user active"), default=False)
    is_superuser = models.BooleanField(_("Is Superuser"), default=False)
    is_staff = models.BooleanField(_("Is staff"), default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_photo(self):
        if self.image:
            return self.image.url
        return "/static/img/no_image.png"

    def get_role(self):
        return self.role.title

    def get_profile(self):
        if self.get_role() == "Volunter":
            return Volunter.objects.get(user=self)
        elif self.get_role() == "Squad":
            return Squad.objects.get(user=self)
        elif self.get_role() == "Admin":
            return Admin.objects.get(user=self)
        return self.email


# admin user model
class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, primary_key=True)
    full_name = models.CharField(_("Full name"), max_length=254)
    passport_id = models.CharField(_("Passport"), max_length=254, null=True, blank=True)
    birthday = models.DateField(_("Birthday"), null=True, blank=True)

    def __str__(self):
        return self.full_name

    def get_photo(self):
        if self.user.image:
            return self.user.image.url
        return "/static/img/no_image.png"


class VolunterType(models.Model):
    name = models.CharField(_("Volunter type name"), max_length=254)

    def __str__(self):
        return self.name


class SquadType(models.Model):
    name = models.CharField(_("Squad type name"), max_length=254)

    def __str__(self):
        return self.name


# volunter user model
class Volunter(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="user_to_volunter",
    )
    full_name = models.CharField(_("Full name"), max_length=254, null=True, blank=True)
    organization_name = models.CharField(
        _("Organization name"), max_length=254, null=True, blank=True
    )
    is_organisation = models.BooleanField(
        _("Is organisation or individual"), default=False
    )
    volunter_type = models.ForeignKey(
        VolunterType, on_delete=models.PROTECT, verbose_name=_("Volunter type name")
    )

    def __str__(self):
        if self.is_organisation:
            return self.organization_name
        return self.full_name

    def get_photo(self):
        if self.user.image:
            return self.user.image.url
        return "/static/img/no_image.png"


# squad user model
class Squad(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name="user_to_squad"
    )
    squad_name = models.CharField(_("squad name"), max_length=254)
    squad_type = models.ForeignKey(
        SquadType, on_delete=models.PROTECT, verbose_name=_("Squad type name")
    )

    def __str__(self):
        return self.squad_name

    def get_photo(self):
        if self.user.image:
            return self.user.image.url
        return "/static/img/no_image.png"
