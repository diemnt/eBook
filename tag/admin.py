# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from tag.models import *
# Register your models here.


class SystemTagAdmin(admin.ModelAdmin):
	pass

admin.site.register(SystemTag, SystemTagAdmin)

class CustomerTagAdmin(admin.ModelAdmin):
	pass

admin.site.register(CustomerTag, CustomerTagAdmin)

class BookTagAdmin(admin.ModelAdmin):
	pass

admin.site.register(BookTag, BookTagAdmin)

# Register your models here.
