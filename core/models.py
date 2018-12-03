# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from main.models import DateTimeAuthModel, DateTimeModel
from autosequence import AutoSequenceField
from django_fsm import FSMField, transition


def book_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return '{0}/{1}/{2}'.format(instance.book_type, instance.name, filename)


def page_book_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return '{0}/{1}/{2}/{3}'.format(instance.book.id, instance.book.book_type, instance.page_number, filename)

# Create your models here.
# @python_2_unicode_compatible
# class Banner(DateTimeModel):
#     POSITION = (
#         (1, 1),
#         (2, 2),
#     )
#     image = models.ImageField(_("Image"), max_length=1000, upload_to=book_directory_path)
#     name = models.CharField(_("Name"), max_length=1000)
#     is_show = models.BooleanField(_("Is Show"), default=False)
#     video = models.FileField(_("Video"), max_length=1000, upload_to=book_directory_path, null=True, blank=True)

#     def __str__(self):
#         return '%s' % (self.name)

#     class Meta:
#         verbose_name = _('Banner')


@python_2_unicode_compatible
class Group(DateTimeModel):
    name = models.CharField(_('Name'), max_length=255)
    description = models.CharField(
        _('Decription'), max_length=255, null=True, blank=True)

    def __str__(self):
        return "%s" % (self.name)


@python_2_unicode_compatible
class Level(DateTimeModel):
    name = models.CharField(_('Name'), max_length=255)
    description = models.CharField(
        _('Decription'), max_length=255, null=True, blank=True)
    is_active = models.BooleanField(_('Is Active'), default=False)
    sequence_number = AutoSequenceField(start_at=1)
    condition = models.IntegerField(
        _('Condition'), default=0,
        help_text=_('Total book must be read to pass this level.')
    )
    group = models.ForeignKey(
        'Group', related_name='group_level_rel', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return "%s" % (self.name)


@python_2_unicode_compatible
class BookCategory(DateTimeModel):
    category_parent = models.ForeignKey(
        'self', related_name='children', on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(_('Name'), max_length=255)
    description = models.CharField(
        _('Decription'), max_length=255, null=True, blank=True)
    is_draft = models.BooleanField(_('Is draft'), default=False)

    def __str__(self):
        return "%s" % (self.name)


@python_2_unicode_compatible
class Book(DateTimeAuthModel):
    BOOK_TYPE = (
        ('book', 'Book'),
        ('video', 'Video'),
    )
    LANGUAGE = (
        ('vie', 'Vietnames'),
        ('eng', 'English')
    )

    class STATE:
        DRAFT = 'draft'
        COMPLETED = 'completed'
        PUBLISHED = 'published'
        DISABLED = 'disabled'

    category = models.ForeignKey(
        'BookCategory', on_delete=models.SET_NULL, null=True, blank=True)
    level = models.ForeignKey(
        'Level', on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(_('Name'), max_length=255)
    book_type = models.CharField(
        _('Book Type'), max_length=250, choices=BOOK_TYPE, default="book")
    language = models.CharField(
        _('Language'), max_length=250, choices=LANGUAGE, default="vie")
    point = models.IntegerField(_('Point'))
    author = models.CharField(
        _('Author'), max_length=255, null=True, blank=True)
    description = models.CharField(
        _('Description'), max_length=255, null=True, blank=True)
    image = models.ImageField(
        _('Image'), upload_to=book_directory_path, null=True, blank=True)
    video = models.FileField(_("Video"), max_length=1000,
                             upload_to=book_directory_path, null=True, blank=True)
    status = FSMField('Status', max_length=250, default=STATE.DRAFT)
    quizz = models.ForeignKey(
        'quizz.Quizz', on_delete=models.SET_NULL, null=True, blank=True)

    @transition(field='status', source=STATE.DRAFT, target=STATE.COMPLETED)
    @transition(field='status', source=STATE.DISABLED, target=STATE.COMPLETED)
    def complete(self):
        pass

    @transition(field='status', source=STATE.DISABLED, target=STATE.DRAFT)
    def draft(self):
        pass

    @transition(field='status', source=STATE.COMPLETED, target=STATE.PUBLISHED)
    def publish(self):
        pass

    @transition(field='status', source=STATE.PUBLISHED, target=STATE.DISABLED)
    def disable(self):
        pass

    def __str__(self):
        return "%s" % (self.name)

    class Meta:
        verbose_name = _('Book')


@python_2_unicode_compatible
class Page(DateTimeAuthModel):
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    content = models.CharField(_('Content'), max_length=255)
    page_number = models.IntegerField(_('Page number'))
    image = models.ImageField(_('Image'), upload_to=page_book_directory_path)
    audio = models.FileField(
        _('Audio'), upload_to=page_book_directory_path, null=True, blank=True)
    timing_mapping = models.FileField(
        _('Timing Mapping'), upload_to=page_book_directory_path, null=True, blank=True)

    def __str__(self):
        return "%s" % (self.book.name)

    class Meta:
        verbose_name = _('Page')
