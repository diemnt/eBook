# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.exceptions import ValidationError
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.db import models
from main.models import DateTimeAuthModel, DateTimeModel, User
from django_fsm import FSMField, transition
from main.models import AbstractBasePackage


@python_2_unicode_compatible
class Package(AbstractBasePackage):

    class STATE:
        DRAFT = 'draft'
        PUBLISH = 'publish'
        UNPUBLISH = 'unpublish'

    book_categories = models.ManyToManyField(
        'core.BookCategory', through='PackagePersonalBookCategory', blank=True, related_name='rel_package_personal_m2m_book_category')
    kid_limit = models.IntegerField(_('Kid Limit'), default=3)
    status = FSMField(default=STATE.DRAFT)

    @transition(field='status', source=STATE.DRAFT, target=STATE.PUBLISH, conditions=[])
    @transition(field='status', source=STATE.UNPUBLISH, target=STATE.PUBLISH, conditions=[])
    def publish(self):
        pass

    @transition(field='status', source=STATE.PUBLISH, target=STATE.UNPUBLISH)
    def unpublish(self):
        pass

    def __str__(self):
        return "%s" % (self.name)

    def delete(self, *args, **kwargs):
        if self.status != self.STATE.DRAFT:
            raise ValidationError(
                "Không thể xoá gói dịch vụ khi đang ở trạng thái %s" % self.status)
        super(Package, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = _('Packages')


@python_2_unicode_compatible
class PackagePersonalBookCategory(DateTimeModel):
    package = models.ForeignKey('Package', on_delete=models.CASCADE)
    book_category = models.ForeignKey(
        'core.BookCategory', on_delete=models.CASCADE)

    def __str__(self):
        return "%s" % (self.package.name)

    class Meta:
        verbose_name = _('Package Personal Book Category')
        unique_together = ("package", "book_category")


@python_2_unicode_compatible
class Personal(DateTimeAuthModel):
    GENDER =(
        ('male', 'Male'),
        ('female', 'Female')
    )

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="user_personal_rel")
    packages = models.ManyToManyField(
        'Package', through='PersonalPackage', blank=True)
    full_name = models.CharField(
        _('Full Name'), max_length=255, null=True, blank=True)
    email = models.CharField(_('Email'), max_length=255)
    gender = models.CharField(max_length=50, choices=GENDER, null=True, blank=True)
    phone = models.CharField(_('Phone'), max_length=255)
    address = models.CharField(
        _('Address'), max_length=255, null=True, blank=True)
    city = models.CharField(_('City'), max_length=255, null=True, blank=True)
    personal_id = models.CharField(
        _('Personal id'), max_length=50, null=True, blank=True)
    avatar = models.ImageField(
        _('Avatar'), upload_to='Personal/Avatar', null=True, blank=True)

    def get_limit_kid(self):
        # TODO code
        return 0

    def __str__(self):
        return "%s" % (self.full_name)

    class Meta:
        verbose_name = _('Personal')


@python_2_unicode_compatible
class PersonalPackage(DateTimeModel):
    package = models.ForeignKey('Package', on_delete=models.CASCADE)
    personal = models.ForeignKey('Personal', on_delete=models.CASCADE)
    expiry_date = models.DateTimeField(_('Expiry Date'))
    # Run cron job to set True/False by exprixed date
    is_active = models.BooleanField(_('Is Active'), default=True)

    def __str__(self):
        return "%s" % (self.package.name)

    class Meta:
        verbose_name = _('Personal Package')
