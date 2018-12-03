# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from personal.models import *

# Register your models here.


class PackagePersonalBookCategoryInline(admin.TabularInline):
    model = PackagePersonalBookCategory

class PackageAdmin(admin.ModelAdmin):
    inlines = (
       PackagePersonalBookCategoryInline,
    )

admin.site.register(Package, PackageAdmin)


class PersonalPackageInline(admin.TabularInline):
    model = PersonalPackage

class PersonalAdmin(admin.ModelAdmin):
    inlines = (
       PersonalPackageInline,
    )

admin.site.register(Personal, PersonalAdmin)

