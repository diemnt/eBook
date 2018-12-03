# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from staff.models import *
# Register your models here.

class StaffRoleInline(admin.TabularInline):
	model = StaffRole

class StaffAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone')
    inlines = (
    	StaffRoleInline,
    )

admin.site.register(Staff, StaffAdmin)

class RoleAdmin(admin.ModelAdmin):
	pass

admin.site.register(Role, RoleAdmin)






