# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils.encoding import python_2_unicode_compatible
from main.models import DateTimeAuthModel, DateTimeModel


@python_2_unicode_compatible
class Kid(AbstractBaseUser):
    GENDER = (
        ('male', 'Male'),
        ('female', 'Female')
    )

    full_name = models.CharField(
        _('Full Name'), max_length=255, null=True, blank=True)
    nickname = models.CharField(
        _('Nick Name'), max_length=255, null=True, blank=True)
    username = models.CharField(
        _('Username'), max_length=255, null=True, blank=True)
    birth_date = models.DateField(_('Birthday'), null=True, blank=True)
    phone = models.CharField(_('Phone'), max_length=50,
                             unique=True, null=True, blank=False)
    gender = models.CharField(
        _('Gender'), max_length=50, choices=GENDER, null=True, blank=True)
    is_active = models.BooleanField(
        _('Active'), default=False,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.')
    )
    avatar = models.ImageField(
        _('Avatar'), upload_to='Kid/Avatar', null=True, blank=True)
    date_joined = models.DateTimeField(_('Date Joined'), auto_now_add=True,
                                       editable=False)
    modified = models.DateTimeField(
        _('Modified Date'), auto_now=True, editable=False)
    personal = models.ForeignKey(
        'personal.Personal', related_name='kid_personal_rel', on_delete=models.CASCADE, null=True, blank=False)
    organization = models.ForeignKey(
        'organization.Organization', related_name='kid_organization_rel', on_delete=models.CASCADE, null=True, blank=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        # The user is identified by their email address
        return self.username

    def get_short_name(self):
        # The user is identified by their email address
        return self.username

    def __str__(self):              # __unicode__ on Python 2
        return self.username

    class Meta:
        app_label = 'kid'


@python_2_unicode_compatible
class BookFavourite(DateTimeModel):
    book = models.ForeignKey('core.Book', on_delete=models.CASCADE)
    kid = models.ForeignKey('Kid', on_delete=models.CASCADE)

    def __str__(self):
        return "%s" % (self.book.name)

    class Meta:
        verbose_name = _('Book Favourite')
        unique_together = ("book", "kid")


@python_2_unicode_compatible
class BookMark(DateTimeModel):
    book = models.ForeignKey('core.Book', on_delete=models.CASCADE)
    kid = models.ForeignKey('Kid', on_delete=models.CASCADE)
    page_number = models.IntegerField(_('Page Number'))

    def __str__(self):
        return "%s" % (self.book.name)

    class Meta:
        verbose_name = _('Book Mark')
        unique_together = ("book", "kid", "page_number")


@python_2_unicode_compatible
class InvitedBook(DateTimeModel):
    book = models.ForeignKey('core.Book', on_delete=models.CASCADE)
    kid = models.ForeignKey('Kid', on_delete=models.CASCADE)
    teacher = models.ForeignKey(
        'organization.Teacher', on_delete=models.CASCADE, null=True, blank=True)
    personal = models.ForeignKey(
        'personal.Personal', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return "%s" % (self.book.name)

    class Meta:
        verbose_name = _('Invited Book')
        unique_together = (("book", "kid", "teacher"),
                           ("book", "kid", "personal"), )


@python_2_unicode_compatible
class Store(DateTimeAuthModel):
    name = models.CharField(_('Name'), max_length=255)
    point = models.IntegerField(_('Point'))
    image = models.ImageField(_('Image'), upload_to='Store')

    def __str__(self):
        return "%s" % (self.name)


@python_2_unicode_compatible
class KidStore(DateTimeModel):
    store = models.ForeignKey('Store', on_delete=models.CASCADE)
    kid = models.ForeignKey('Kid', on_delete=models.CASCADE)

    def __str__(self):
        return "%s" % (self.store.name)

    class Meta:
        verbose_name = _('Kid Store')
        unique_together = ("store", "kid")


@python_2_unicode_compatible
class KidReadBookTrack(DateTimeModel):
    STATUS = (
        ('reading', 'Reading'),
        ('done', 'Done')
    )
    book = models.ForeignKey('core.Book', on_delete=models.CASCADE)
    kid = models.ForeignKey('Kid', on_delete=models.CASCADE)
    status = models.CharField(
        _('Status'), max_length=50, choices=STATUS, default="reading")
    page_number = models.IntegerField(_('Page Number'), null=True, blank=True)

    def __str__(self):
        return "%s" % (self.page_number)
