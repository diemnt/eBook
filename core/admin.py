# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from core.models import *

class GroupAdmin(admin.ModelAdmin):
    pass
admin.site.register(Group, GroupAdmin)

class LevelAdmin(admin.ModelAdmin):
    list_display = ('name' ,'group', 'sequence_number')
    readonly_fields = ('sequence_number',)

admin.site.register(Level, LevelAdmin)

class BookCategoryAdmin(admin.ModelAdmin):
    pass
admin.site.register(BookCategory, BookCategoryAdmin)

class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')

admin.site.register(Book, BookAdmin)

class PageAdmin(admin.ModelAdmin):
    pass
admin.site.register(Page, PageAdmin)

