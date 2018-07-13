# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Item, PriceLevel, PriceLevelPerItem, Category, UnitOfMeasure, UnitOfPackage, Group
# Register your models here.

class ItemAdmin(admin.ModelAdmin):
    list_display = ('id','fullname', 'description','group','category','unitofmeasure','unitofpackage','isactive')
    list_display_links = ('id','fullname')
    list_filter = ['category','group','unitofmeasure','isactive']
    search_fields = ['name','description']
    list_select_related = ['group','category','unitofmeasure','unitofpackage']
    radio_fields = {'group':admin.HORIZONTAL}

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name']
    list_display_links = ['id','name']
    ordering = ['id']


class PriceLevelPerItemAdmin(admin.ModelAdmin):
    list_display = ['pricelevel','item','customprice']
    list_display_links = ['item']
    list_select_related = ['item','pricelevel']
    list_filter = ['pricelevel']

class PriceLevelAdmin (admin.ModelAdmin):
    list_display = ['name','QuickbookListId','isactive']
    list_display_links = ['name']
    list_editable = ['isactive']

admin.site.register(Item,ItemAdmin)
admin.site.register(PriceLevel, PriceLevelAdmin)
admin.site.register(PriceLevelPerItem, PriceLevelPerItemAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(UnitOfMeasure)
admin.site.register(UnitOfPackage)
admin.site.register(Group)