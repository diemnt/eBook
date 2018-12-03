# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.db import models
# from staff.fields import CurrentStaffField

# Create your models here.


class DateTimeModel(models.Model):
    created_date = models.DateTimeField(_('Created Date'), auto_now_add=True,
                                        editable=False)
    modified_date = models.DateTimeField(
        _('Modified Date'), auto_now=True, editable=False)

    class Meta:
        abstract = True


class DateTimeAuthModel(DateTimeModel):
    created_by = models.ForeignKey(
        'staff.Staff', on_delete=models.SET_NULL, related_name="%(app_label)s_%(class)s_created_by", null=True, blank=True)

    modified_by = models.ForeignKey(
        'staff.Staff', on_delete=models.SET_NULL, related_name="%(app_label)s_%(class)s_modified_by", null=True, blank=True)

    class Meta:
        abstract = True


class AbstractBasePackage(DateTimeAuthModel):
    name = models.CharField(_('Name'), max_length=255)
    description = models.CharField(
        _('Decription'), max_length=255, null=True, blank=True)
    price = models.IntegerField(_('Price'))
    effective_time = models.IntegerField(
        _('Effective Time'), default=0)  # Month
    is_trial = models.BooleanField("Trial", default=False)

    class Meta:
        abstract = True


class EbookUserManager(BaseUserManager):

    def create_user(self, username, password=None, email=None, **extra_fields):
        print "create_user:::"
        """
        Creates and saves a User with the given email and password.
        """
        user = self.model(
            email=self.normalize_email(email),
            **extra_fields
        )
        # print "email ",email
        user.username = username if username else email
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            username,
            password=password
        )
        user.username = username
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user

    class Meta:
        app_label = 'main'


class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(
        _('Username'), max_length=255, unique=True)
    email = models.CharField(max_length=255, null=True, blank=True)

    is_staff = models.BooleanField(
        _('Staff Status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.')
    )
    is_active = models.BooleanField(
        _('Active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.')
    )
    date_joined = models.DateTimeField(_('Date Joined'), auto_now_add=True,
                                       editable=False)
    modified = models.DateTimeField(
        _('Modified Date'), auto_now=True, editable=False)

    objects = EbookUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        # The user is identified by their username
        return self.username

    def get_short_name(self):
        # The user is identified by their username
        return self.username

    def __str__(self):              # __unicode__ on Python 2
        return self.username

    class Meta:
        app_label = 'main'
        verbose_name = _('User')
