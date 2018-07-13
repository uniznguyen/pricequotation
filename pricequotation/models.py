# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class UnitOfMeasure(models.Model):
    name = models.CharField(max_length=200, unique=True)
    def __str__(self):
        return self.name

class UnitOfPackage(models.Model):
    name = models.CharField(max_length=200, unique=True)
    def __str__(self):
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=200,unique=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class PriceLevel(models.Model):
    name = models.CharField(max_length=200, unique=True)
    QuickbookListId = models.CharField(max_length=200, null=True, unique=True)
    isactive = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=200, unique=True)
    fullname = models.CharField(max_length=200,unique=True, null=True)
    description = models.CharField(max_length=200)
    group = models.ForeignKey(Group, on_delete=models.PROTECT, null=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True)
    salesprice = models.DecimalField(decimal_places=2, max_digits=10)
    QuickbookListID = models.CharField(max_length=200, null=True,unique=True)
    productcode = models.CharField(max_length=200, null=True, blank=True)
    unitofmeasure = models.ForeignKey(UnitOfMeasure, on_delete=models.PROTECT, null=True)
    unitofpackage = models.ForeignKey(UnitOfPackage, on_delete=models.PROTECT, null=True)
    isactive = models.BooleanField(default=True)
    remark = models.CharField(max_length=200,null=True,blank=True)

    def __str__(self):
        return self.name +"-"+ self.description



class PriceLevelPerItem(models.Model):
    pricelevel = models.ForeignKey(PriceLevel,on_delete=models.PROTECT)
    item = models.ForeignKey(Item,on_delete=models.PROTECT)
    customprice = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return self.item.name +'-'+ self.pricelevel.name +'-'+ str(self.customprice)

class JoinPriceLevelPerItem(models.Model):
    name = models.CharField(max_length=200)
    fullname = models.CharField ( max_length=200, null=True)
    description = models.CharField (max_length=200)
    itemlistid = models.CharField (max_length=200 , null=True, unique=False)
    pricelevelname = models.CharField (max_length=200 , null=True)
    pricelevellistid = models.CharField (max_length=200 , null=True)
    customprice = models.DecimalField(decimal_places=2, max_digits=10)
