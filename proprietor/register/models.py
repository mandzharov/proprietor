import re
from datetime import date
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.hashers import make_password


def phone_validator(value):
    pattern = r'^[1-9]\d{6,8}$'
    if not re.findall(pattern, value):
        raise ValidationError('Please, enter a valid phone number. Only numbers allowed.')


def country_code_validator(value):
    pattern = r'^(?:\+|00)[1-9]\d{1,2}$'
    if not re.findall(pattern, value):
        raise ValidationError('Please, enter a valid country code. Should start with + or 00.')


class AppManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class AppUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    created_dt = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = AppManager()

    def __str__(self) -> str:
        return str(self.email)


class CountryCodes(models.Model):
    name = models.CharField(max_length=30)
    code = models.CharField(max_length=6, blank=False, null=False, validators=[country_code_validator])

    def __str__(self):
        return str(self.code)


class Profile(models.Model):
    GENDERS = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('LGTB', 'LGTB'),
    ]
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30)
    birth_date = models.DateField()
    gender = models.CharField(max_length=30, choices=GENDERS, default=GENDERS[0][0])
    phone = models.CharField(max_length=9, validators=[phone_validator])
    picture = models.ImageField(null=True, blank=True)
    phone_code = models.ForeignKey(CountryCodes, on_delete=models.PROTECT)
    user = models.OneToOneField(AppUser, primary_key=True, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name} {self.user}'

    @property
    def age(self):
        today = date.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
