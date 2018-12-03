# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.postgres.fields import ArrayField
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.db import models
from main.models import DateTimeAuthModel, DateTimeModel
from django.contrib.auth.models import User

# Create your models here.
@python_2_unicode_compatible
class SystemTag(DateTimeModel):
    name = models.CharField(_('Name'), max_length=255)
    description = models.CharField(_('Decription'), max_length=255, null=True, blank=True)
    owner_id =  models.CharField(_('Owner ID'), max_length=255, null=True, blank=True)
    owner_username =  models.CharField(_('Owner Username'), max_length=255, null=True, blank=True)
    is_draft = models.BooleanField(_('Is Draft'), default=False)

    def __str__(self):
        return "%s" % (self.name)

    class Meta:
        verbose_name = _('System Tag')
        unique_together = ("name", "owner_id")

@python_2_unicode_compatible
class CustomerTag(DateTimeModel):
    CUSTOMER_TYPE = (
        ('kid', 'Kid'),
        ('teacher', 'Teacher'),
        ('personal', 'Personal')
    )
    name = models.CharField(_('Name'), max_length=255)
    description = models.CharField(_('Decription'), max_length=255, null=True, blank=True)
    owner_id =  models.CharField(_('Owner ID'), max_length=255, null=True, blank=True)
    owner_username =  models.CharField(_('Owner Username'), max_length=255, null=True, blank=True)
    customer_type = models.CharField('Customer Type', max_length=255, choices=CUSTOMER_TYPE, default="kid")

    def __str__(self):
        return "%s" % (self.name)

    class Meta:
        verbose_name = _('Customer Tag')
        unique_together = ("name", "owner_id", "customer_type")

@python_2_unicode_compatible
class BookTag(DateTimeModel):
    book_id = models.CharField(_('Book ID'), max_length=255, null=True, blank=True)
    system_tag_list = models.TextField(_('Customer Tag List'), null=True, blank=True)
    customer_tag_list = models.TextField(_('Customer Tag List'), null=True, blank=True)
   
    def __str__(self):
        return "%s" % (self.tag_name)
        
    class Meta:
        verbose_name = _('Book Tag')