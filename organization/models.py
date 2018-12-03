# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.db import models
from main.models import DateTimeAuthModel, DateTimeModel, User
from django.contrib.auth.models import AbstractBaseUser
from django_fsm import FSMField, transition
from main.models import AbstractBasePackage

# Create your models here.


@python_2_unicode_compatible
class Package(AbstractBasePackage):

    class STATE:
        DRAFT = 'draft'
        PUBLISH = 'publish'
        UNPUBLISH = 'unpublish'

    book_categories = models.ManyToManyField(
        'core.BookCategory', through='PackageOrganizationBookCategory', blank=True, related_name='rel_package_organization_m2m_book_category')
    kid_limit_default = models.IntegerField(_('Kid Limit Default'), default=0)
    teacher_limit_default = models.IntegerField(
        _('Teacher Limit Default'), default=0)
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

    def __str__(self):
        return "%s" % (self.name)

    class Meta:
        verbose_name = _('Packages')


@python_2_unicode_compatible
class PackageOrganizationBookCategory(DateTimeModel):
    package = models.ForeignKey('Package', on_delete=models.CASCADE)
    book_category = models.ForeignKey(
        'core.BookCategory', on_delete=models.CASCADE)

    def __str__(self):
        return "%s" % (self.package.name)

    class Meta:
        verbose_name = _('Package Book Category')
        unique_together = ("package", "book_category")


@python_2_unicode_compatible
class Organization(DateTimeAuthModel):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="user_organization_rel")
    packages = models.ManyToManyField(
        'Package', through='OrganizationPackage', blank=True)
    full_name = models.CharField(
        _('Full Name'), max_length=255, null=True, blank=True)
    email = models.CharField(_('Email'), max_length=255)
    phone = models.CharField(_('Phone'), max_length=255)
    address = models.CharField(
        _('Address'), max_length=255, null=True, blank=True)
    city = models.CharField(_('City'), max_length=255, null=True, blank=True)
    tax_code = models.CharField(_('Tax Code'), max_length=255)
    kid_limit = models.IntegerField(_('Kid Limit'), default=0)
    teacher_limit = models.IntegerField(_('Teacher Limit'), default=0)
    avatar = models.ImageField(
        _('Avatar'), upload_to='Organization/Avatar', null=True, blank=True)

    def __str__(self):
        return "%s" % (self.user.username)

    class Meta:
        verbose_name = _('Customer Organization')


@python_2_unicode_compatible
class Management(DateTimeModel):
    organization = models.OneToOneField(
        'Organization', on_delete=models.CASCADE)
    email = models.EmailField(_('Email'), max_length=255)
    phone = models.CharField(_('Phone'), max_length=255)
    full_name = models.CharField(_('Full Name'), max_length=255)
    address = models.CharField(
        _('Address'), max_length=255, null=True, blank=True)
    city = models.CharField(_('City'), max_length=255, null=True, blank=True)

    def __str__(self):
        return "%s" % (self.email)

    class Meta:
        verbose_name = _('Customer Management')


@python_2_unicode_compatible
class OrganizationPackage(DateTimeModel):
    package = models.ForeignKey('Package', on_delete=models.CASCADE)
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE)
    order_id = models.CharField(_('Order ID'), max_length=100)
    expiry_date = models.DateTimeField(_('Expiry Date'))
    # Run cron job to set True/False by exprixed date
    is_active = models.BooleanField(_('Is Active'), default=True)


    def __str__(self):
        return "%s" % (self.package.name)

    class Meta:
        verbose_name = _('Organization Package')


@python_2_unicode_compatible
class Parent(AbstractBaseUser):
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE)
    kids = models.ManyToManyField(
        'kid.Kid', through='ParentKid', blank=True)
    email = models.EmailField(
        _('Email'), max_length=255, null=True, blank=True)
    username = models.CharField(_('User Name'), max_length=255)
    phone = models.CharField(_('Phone'), max_length=255, null=True, blank=True)
    dob = models.DateTimeField(_('Created Date'), null=True, blank=True)
    full_name = models.CharField(
        _('Full Name'), max_length=255, null=True, blank=True)
    address = models.CharField(
        _('Address'), max_length=255, null=True, blank=True)
    city = models.CharField(_('City'), max_length=255, null=True, blank=True)
    personal_id = models.CharField(
        _('Personal Id'), max_length=255, null=True, blank=True)
    avatar = models.ImageField(
        _('Avatar'), upload_to='Parent/Avatar', null=True, blank=True)
    date_joined = models.DateTimeField(_('Date Joined'), auto_now_add=True,
                                       editable=False)
    modified = models.DateTimeField(
        _('Modified Date'), auto_now=True, editable=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return "%s" % (self.email)

    class Meta:
        verbose_name = _('Parent Organization')


@python_2_unicode_compatible
class ParentKid(DateTimeModel):
    parent = models.ForeignKey('Parent', on_delete=models.CASCADE)
    kid = models.ForeignKey('kid.Kid', on_delete=models.CASCADE)

    def __str__(self):
        return "%s" % (self.kid.full_name)

    class Meta:
        verbose_name = _('Customer  Package')
        unique_together = ("parent", "kid")


@python_2_unicode_compatible
class Teacher(AbstractBaseUser):
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE)
    kids = models.ManyToManyField(
        'kid.Kid', through='ClassRoom', related_name='teacher_kid_rel', blank=True)
    username = models.CharField(_('User Name'), max_length=255)
    email = models.EmailField(
        _('Email'), max_length=255, null=True, blank=True)
    phone = models.CharField(_('Phone'), max_length=255, null=True, blank=True)
    dob = models.DateTimeField(_('Created Date'), null=True, blank=True)
    full_name = models.CharField(
        _('Full Name'), max_length=255, null=True, blank=True)
    address = models.CharField(
        _('Address'), max_length=255, null=True, blank=True)
    city = models.CharField(_('City'), max_length=255, null=True, blank=True)
    personal_id = models.CharField(
        _('Personal Id'), max_length=255, null=True, blank=True)
    avatar = models.ImageField(
        _('Avatar'), upload_to='Teacher/Avatar', null=True, blank=True)
    date_joined = models.DateTimeField(_('Date Joined'), auto_now_add=True,
                                       editable=False)
    modified = models.DateTimeField(
        _('Modified Date'), auto_now=True, editable=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return "%s" % (self.email)

    class Meta:
        verbose_name = _('Teacher')


@python_2_unicode_compatible
class ClassRoom(DateTimeModel):
    name = models.CharField(_('Name'), max_length=255)
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE)
    kid = models.ForeignKey('kid.Kid', on_delete=models.CASCADE)

    def __str__(self):
        return "%s" % (self.name)

    class Meta:
        verbose_name = _('ClassRoom')
