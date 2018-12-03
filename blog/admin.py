# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from blog.models import *
from django.contrib import admin
# Register your models here.


class PostAdmin(admin.ModelAdmin):
    pass
admin.site.register(Post, PostAdmin)


