# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-11 19:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('fullname', models.CharField(max_length=200, null=True, unique=True)),
                ('description', models.CharField(max_length=200)),
                ('salesprice', models.DecimalField(decimal_places=2, max_digits=10)),
                ('QuickbookListID', models.CharField(max_length=200, null=True, unique=True)),
                ('productcode', models.CharField(blank=True, max_length=200, null=True)),
                ('isactive', models.BooleanField(default=True)),
                ('remark', models.CharField(blank=True, max_length=200, null=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='pricequotation.Category')),
                ('group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='pricequotation.Group')),
            ],
        ),
        migrations.CreateModel(
            name='JoinPriceLevelPerItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('fullname', models.CharField(max_length=200, null=True)),
                ('description', models.CharField(max_length=200)),
                ('itemlistid', models.CharField(max_length=200, null=True)),
                ('pricelevelname', models.CharField(max_length=200, null=True)),
                ('pricelevellistid', models.CharField(max_length=200, null=True)),
                ('customprice', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='PriceLevel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('QuickbookListId', models.CharField(max_length=200, null=True, unique=True)),
                ('isactive', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='PriceLevelPerItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customprice', models.DecimalField(decimal_places=2, max_digits=10)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pricequotation.Item')),
                ('pricelevel', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pricequotation.PriceLevel')),
            ],
        ),
        migrations.CreateModel(
            name='UnitOfMeasure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='UnitOfPackage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='unitofmeasure',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='pricequotation.UnitOfMeasure'),
        ),
        migrations.AddField(
            model_name='item',
            name='unitofpackage',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='pricequotation.UnitOfPackage'),
        ),
    ]