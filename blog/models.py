# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.db import models
from main.models import DateTimeAuthModel

# Create your models here.
@python_2_unicode_compatible
class Post(DateTimeAuthModel):
    POST_TYPE = (
        ('events', 'Events'),
        ('news', 'News'),
        ('promotions', 'Promotions'),
    )
    name = models.CharField(_("Name"), max_length=255)
    content = models.TextField(_("Content"))
    image = models.ImageField(_("Image"), max_length=1000, upload_to='Post')
    is_draft = models.BooleanField(default=False)
    post_type = models.CharField(_('Post Type'), max_length=250, choices=POST_TYPE, default="news")

    def __str__(self):
        return '%s' % (self.name)

    class Meta:
        verbose_name = _('Post')