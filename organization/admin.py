# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from organization.models import *

# Register your models here.

class PackageOrganizationBookCategoryInline(admin.TabularInline):
    model = PackageOrganizationBookCategory

class PackageAdmin(admin.ModelAdmin):
    inlines = (
       PackageOrganizationBookCategoryInline,
    )
admin.site.register(Package, PackageAdmin)

class OrganizationPackageInline(admin.TabularInline):
    model = OrganizationPackage

class OrganizationAdmin(admin.ModelAdmin):
    inlines = (
        OrganizationPackageInline,
	)

    list_display = ('user', 'phone')

admin.site.register(Organization, OrganizationAdmin)

class ManagementAdmin(admin.ModelAdmin):
    list_display = ('email', 'organization')

admin.site.register(Management, ManagementAdmin)


class ParentKidInline(admin.TabularInline):
    model = ParentKid

class ParentAdmin(admin.ModelAdmin):
    inlines = (
        ParentKidInline,
	)
    list_display = ('username', 'organization')

admin.site.register(Parent, ParentAdmin)

class ClassRoomInline(admin.TabularInline):
    model = ClassRoom

class TeacherAdmin(admin.ModelAdmin):
    inlines = (
        ClassRoomInline,
	)
    list_display = ('username', 'organization')

admin.site.register(Teacher, TeacherAdmin)

class ClassRoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher', 'kid')

admin.site.register(ClassRoom, ClassRoomAdmin)

