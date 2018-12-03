# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# from django.contrib.auth.forms import UserCreationForm, UserChangeForm
# from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
# from django.contrib.auth.models import User
from django.contrib import admin

# Import admin site
from badge.admin import *
# from blog.admin import *
from core.admin import *
from kid.admin import *
# from notification.admin import *
from organization.admin import *
from personal.admin import *
from quizz.admin import *
from staff.admin import *
# from tag.admin import *


# class UserAdmin(UserAdmin):
#     add_form = UserCreationForm
#     form = UserChangeForm
#     fieldsets = (
#         (None, {'fields': ('username', 'email', 'password')}),
#         (_('Personal info'), {'fields': ('first_name', 'last_name')}),
#         (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',)}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('username', 'password1', 'password2'),
#         }),
#     )
#     list_display = ('username', 'email', 'is_active', 'is_staff', 'is_superuser')
#     search_fields = ('email', 'first_name', 'last_name')
#     ordering = ('email',)

# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)




