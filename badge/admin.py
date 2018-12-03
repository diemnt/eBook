# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from badge.models import *
from django.contrib import admin
# Register your models here.

class KidBadgeInline(admin.TabularInline):
    model = KidBadge

class BadgeAdmin(admin.ModelAdmin):
    inlines = (
       KidBadgeInline,
    )
admin.site.register(Badge, BadgeAdmin)

class TimesReadBookAdmin(admin.ModelAdmin):
    pass
admin.site.register(TimesReadBook, TimesReadBookAdmin)