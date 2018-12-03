# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from django.db import models
from main.models import DateTimeAuthModel, DateTimeModel

# Create your models here.


@python_2_unicode_compatible
class Badge(DateTimeAuthModel):
    BADGE_TYPE = (
        ('point', 'Point'),
        ('time', 'Time'),
        ('total', 'Total Book'),
    )
    name = models.CharField('name', max_length=255)
    # Using for app
    name_optional = models.CharField(
        _('Name Optional'), max_length=255, null=True, blank=True)
    badge_type = models.CharField(
        _('Badge Type'), max_length=250, choices=BADGE_TYPE, default="point")
    condition_received = models.CharField(
        _('Condition Recieved'), max_length=255)
    point_received = models.CharField(_('Point Recieved'), max_length=255)
    image = models.ImageField(_('Image'), upload_to='Badge')
    is_active = models.BooleanField(_('Is Active'), default=False)

    def __str__(self):
        return "%s" % (self.name)

    class Meta:
        verbose_name = _('Badge')


@python_2_unicode_compatible
class KidBadge(DateTimeModel):
    badge = models.ForeignKey(
        'Badge', related_name="kidbadges_badges_rel", on_delete=models.CASCADE)
    kid = models.ForeignKey(
        'kid.Kid', related_name="kidbadges_kids_rel", on_delete=models.CASCADE)

    def __str__(self):
        return "%s" % (self.badge.name)

    class Meta:
        verbose_name = _('Kid Badge')
        unique_together = ("badge", "kid")

# Using to get badges with type date


@python_2_unicode_compatible
class TimesReadBook(DateTimeModel):
    kid = models.ForeignKey(
        'kid.Kid', related_name="times_readbook_kids_rel", on_delete=models.CASCADE)
    last_readbook_date = models.DateField(_('Last Read Book Date'))
    count_date = models.IntegerField(_('Count Date'), default=0)

    def __str__(self):
        return "%s" % (self.kid.full_name)

    class Meta:
        verbose_name = _('Times Read Book')
