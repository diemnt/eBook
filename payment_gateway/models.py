# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import User
from main.models import DateTimeAuthModel, DateTimeModel
from django.contrib.auth.models import AbstractBaseUser


# Create your models here.
@python_2_unicode_compatible
class PersonalTransactionTrack(DateTimeAuthModel):
    TRANSACTION_STATUS = (
        ('pending', 'Pending'),
        ('cancel', 'Cancel'),
        ('error', 'Error'),
        ('done', 'Done'),
    )
    package = models.ForeignKey('personal.Package', on_delete=models.CASCADE)
    personal = models.ForeignKey('personal.Personal', on_delete=models.CASCADE)
    order_id = models.CharField(_('Order ID'), max_length=100)
    amount = models.FloatField(_('Amount'))
    status = models.CharField(
        _('Status'), max_length=250, choices=TRANSACTION_STATUS, default="pending")

    def __str__(self):
        return "%s" % (self.status)


@python_2_unicode_compatible
class OrganizationTransactionTrack(DateTimeAuthModel):
    TRANSACTION_STATUS = (
        ('pending', 'Pending'),
        ('cancel', 'Cancel'),
        ('error', 'Error'),
        ('done', 'Done'),
    )
    package = models.ForeignKey(
        'organization.Package', on_delete=models.CASCADE)
    organization = models.ForeignKey(
        'organization.Organization', on_delete=models.CASCADE)
    order_id = models.CharField(_('Order ID'), max_length=100)
    amount = models.FloatField(_('Amount'))
    status = models.CharField(
        _('Status'), max_length=250, choices=TRANSACTION_STATUS, default="pending")

    def __str__(self):
        return "%s" % (self.status)

    class Meta:
        abstract = True
