from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from simple_history.models import HistoricalRecords
from rest_framework import serializers

from apps.base.models import Common


class UserManager(BaseUserManager):
    def _create_user(self, username, email, name, last_name, password, is_staff, is_superuser, **extra_fields):
        user = self.model(
            username=username,
            email=email,
            name=name,
            last_name=last_name,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, username, email, name, last_name, password=None, **extra_fields):
        return self._create_user(username, email, name, last_name, password, False, False, **extra_fields)

    def create_superuser(self, username, email, name, last_name, password=None, **extra_fields):
        return self._create_user(username, email, name, last_name, password, True, True, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, Common):
    MALE = 'Male'
    FEMALE = 'Female'
    genderChoices = (
        (MALE, 'Male'),
        (FEMALE, 'Female')
    )
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField('Email', max_length=255, unique=True,)
    name = models.CharField('Nombre(s)', max_length=255, blank=True, null=True)
    last_name = models.CharField('Apellidos', max_length=255, blank=True, null=True)
    date_of_birth = models.DateField('Fecha de nacimiento', max_length=255, blank=True, null=True, default='1980-01-01')
    address = models.TextField('Dirección', blank=True, null=True)
    phone = models.CharField('Telefono', max_length=10, blank=True, null=True)
    gender = models.CharField('Genero', max_length=40, choices=genderChoices, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    historical = HistoricalRecords()
    objects = UserManager()

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'name', 'last_name']

    def __str__(self):
        return f'{self.name} {self.last_name}'
    