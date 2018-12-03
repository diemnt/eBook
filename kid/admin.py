# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from kid.models import *

# Register your models here.


class BookFavouriteInline(admin.TabularInline):
    model = BookFavourite

class BookMarkInline(admin.TabularInline):
    model = BookMark

class InvitedBookInline(admin.TabularInline):
    model = InvitedBook

class KidStoreInline(admin.TabularInline):
    model = KidStore

class KidReadBookTrackInline(admin.TabularInline):
    model = KidReadBookTrack

class KidAdmin(admin.ModelAdmin):
    inlines = (
       BookFavouriteInline,
       BookMarkInline,
       InvitedBookInline,
       KidStoreInline,
       KidReadBookTrackInline
    )
    list_display = ('username', )
    
admin.site.register(Kid, KidAdmin)

class StoreAdmin(admin.ModelAdmin):
    pass
admin.site.register(Store, StoreAdmin)

class KidReadBookTrackAdmin(admin.ModelAdmin):
    list_display = ('kid', 'book')
admin.site.register(KidReadBookTrack, KidReadBookTrackAdmin)


