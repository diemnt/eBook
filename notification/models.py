# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.db import models
from main.models import DateTimeAuthModel, DateTimeModel, User
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.


@python_2_unicode_compatible
class Notification(DateTimeModel):
    subject = models.CharField(_('Subject'), max_length=255, unique=True)
    message = models.TextField(_('Message'))
    image = models.ImageField(
        _('Image'), max_length=1000, null=True, blank=True, upload_to='Notification')

    def __str__(self):
        return '%s' % (self.subject)

    class Meta:
        verbose_name = _('Notification')


@python_2_unicode_compatible
class NotificationUser(DateTimeModel):
    notification = models.ForeignKey("Notification", on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    teacher = models.ForeignKey(
        "organization.Teacher", on_delete=models.CASCADE, null=True, blank=True)
    parent = models.ForeignKey(
        "organization.Parent", on_delete=models.CASCADE, null=True, blank=True)
    kid = models.ForeignKey(
        "kid.Kid", on_delete=models.CASCADE, null=True, blank=True)
    sent_date = models.DateTimeField(_('Sent Date'), null=True, blank=True)

    def __str__(self):
        return '%s' % (self.notification.subject)

    class Meta:
        verbose_name = _('Notification User')
