# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from notification.models import *

# Register your models here.


class NotificationUserInline(admin.TabularInline):
    model = NotificationUser

class NotificationAdmin(admin.ModelAdmin):
    inlines = (
       NotificationUserInline,
    )
admin.site.register(Notification, NotificationAdmin)

class NotificationUserAdmin(admin.ModelAdmin):
    list_display = ('notification', 'user', 'teacher', 'parent', 'kid')

admin.site.register(NotificationUser, NotificationUserAdmin)


