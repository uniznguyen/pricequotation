# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404, get_list_or_404,redirect
from .models import Item, PriceLevel, PriceLevelPerItem, Category, Group, JoinPriceLevelPerItem
import pyodbc
import datetime
import sqlite3 as db


# test commit
# Create your views here.



def detail(request,selected_pricelevel,group_name,*args,**kwargs):
    selected_items = request.session['selected_items']
    customer_name = request.session['customer_name']

    selected_pricelevel = get_object_or_404(PriceLevel, name=selected_pricelevel)

    pricelevelperitem = (PriceLevelPerItem.objects.select_related('item__category','item__unitofmeasure','item__unitofpackage')
                         .filter(pricelevel__name__exact=selected_pricelevel, item__name__in=selected_items)
                         .order_by('item__category','item__productcode','item__name'))

    return render(request,"detail.html",context={'pricelevelperitem':pricelevelperitem,'selected_pricelevel':selected_pricelevel,
                                                 'group_name':group_name,'customer_name':customer_name})

def listgroup(request,group_name):

    item = Item.objects.select_related('category','unitofmeasure','unitofpackage')\
        .filter(isactive=True , group__name=group_name )\
        .order_by('category' , 'productcode' ,'unitofmeasure')
    pricelevels = get_list_or_404(PriceLevel, isactive = True)

    group = Group.objects.get(name=group_name)

    if request.method == 'POST':
        selected_pricelevel = request.POST['selected_pricelevel']
        selected_items = request.POST.getlist('selected_items')
        customer_name = request.POST['customer_name']

        selected_pricelevel = get_object_or_404(PriceLevel , pk=selected_pricelevel)

        request.session['selected_items'] = selected_items
        request.session['customer_name'] = customer_name

        return redirect('pricequotation:detail', selected_pricelevel=selected_pricelevel,group_name = group_name)
    else:
        return render(request,"main.html",context={'item':item,'pricelevels':pricelevels, 'group':group})


def index2(request):
    groups = get_list_or_404(Group)
    return render(request,"index2.html", context={'groups':groups})


def updateitem(request):
    def getitemsquickbooklistID():
        db_filename = 'db.sqlite3'
        cn2 = db.connect(db_filename)
        cursor2 = cn2.cursor()

        cursor2.execute("""Select QuickbookListID FROM pricequotation_item""")

        items_quickbooklistIDs = ()
        items_quickbooklistIDs = tuple(row[0] for row in cursor2.fetchall())

        cursor2.close()
        cn2.close()
        return items_quickbooklistIDs

    def getpricelevelQuickbookListID():
        db_filename = 'db.sqlite3'
        cn2 = db.connect(db_filename)
        cursor2 = cn2.cursor()
        cursor2.execute("""Select QuickbookListID from pricequotation_pricelevel""")

        pricelevels_quickbooklistIDs = tuple(row[0] for row in cursor2.fetchall())

        cursor2.close()
        cn2.close()
        return pricelevels_quickbooklistIDs

    def getpricelevelperitem(items_quickbooklistIDs, pricelevels_quickbooklistIDs):
        cn1 = pyodbc.connect('DSN=QuickBooks Data;')
        cursor1 = cn1.cursor()

        db_filename = 'db.sqlite3'
        cn2 = db.connect(db_filename)
        cursor2 = cn2.cursor()

        cursor1.execute("""SELECT A.ListID ItemID, A.Name, A.FullName, A.SalesDesc, B.ListID PriceLevelListID, 
        B.Name PriceLevelName, B.PriceLevelPerItemCustomPrice FROM ItemInventoryAssembly A INNER JOIN PriceLevelPerItem B
        ON A.ListID = B.PriceLevelPerItemItemRefListID WHERE A.ListID IN %s AND B.ListID IN %s""" %(str(items_quickbooklistIDs), str(pricelevels_quickbooklistIDs)))

        params = []
        params = list((str(row.Name), str(row.FullName), str(row.SalesDesc), str(row.ItemID), str(row.PriceLevelName),
                       str(row.PriceLevelListID), float(row.PriceLevelPerItemCustomPrice)) for row in
                      cursor1.fetchall())

        cursor2.execute("Delete FROM pricequotation_joinpricelevelperitem")
        cursor2.execute("DELETE FROM sqlite_sequence where name = 'pricequotation_joinpricelevelperitem'")
        cursor2.executemany("""INSERT INTO pricequotation_joinpricelevelperitem (name, fullName, description, itemlistid, pricelevelname, pricelevellistid, customprice)
            VALUES (?,?,?,?,?,?,?)""", params)
        cn2.commit()

        cursor1.close()
        cn1.close()

        cursor2.close()
        cn2.close()

    def updatepricelevelperitem():
        db_filename = 'db.sqlite3'
        cn2 = db.connect(db_filename)
        cursor2 = cn2.cursor()

        cursor2.execute("""select a.id item_id, a.name item_name, b.id pricelevel_id, b.name pricelevel_name, c.customprice
        from pricequotation_item a INNER JOIN pricequotation_joinpricelevelperitem c ON a.QuickbookListID = c.itemlistid
        INNER JOIN pricequotation_pricelevel b ON b.QuickbookListId = c.pricelevellistid""")

        params = list((int(row[0]), int(row[2]), float(row[4])) for row in cursor2.fetchall())

        cursor2.execute("""DELETE FROM pricequotation_pricelevelperitem""")
        cursor2.execute("DELETE FROM sqlite_sequence where name = 'pricequotation_pricelevelperitem'")
        cursor2.executemany(
            """INSERT INTO pricequotation_pricelevelperitem (item_id, pricelevel_id, customprice) VALUES (?,?,?)""",
            params)
        cn2.commit()

        cursor2.close()
        cn2.close()

    def updateitem():
        cn1 = pyodbc.connect('DSN=QuickBooks Data;')
        cursor1 = cn1.cursor()

        db_filename = 'db.sqlite3'
        cn2 = db.connect(db_filename)
        cursor2 = cn2.cursor()

        cursor2.execute("SELECT QuickbookListID FROM pricequotation_item")
        listid = tuple((row[0]) for row in cursor2.fetchall())

        cursor1.execute(
            "SELECT ListID, SalesPrice, SalesDesc, Name, FullName, IsActive FROM ItemInventoryAssembly UNOPTIMIZED WHERE ListID IN %s" % str(listid))

        itemlist = tuple((float(row.SalesPrice), str(row.SalesDesc),str(row.Name), str(row.FullName), row.IsActive, str(row.ListID)) for row in cursor1.fetchall())

        cursor2.executemany("UPDATE pricequotation_item SET salesprice = ?, description = ?, name = ?, fullname = ?, isactive = ? WHERE QuickbookListID = ?",
                            itemlist)
        cn2.commit()

        cursor1.close()
        cn1.close()
        cursor2.close()
        cn2.close()

    starttime = datetime.datetime.now()
    updateitem()
    getpricelevelperitem(getitemsquickbooklistID(), getpricelevelQuickbookListID())
    updatepricelevelperitem()
    endtime = datetime.datetime.now()
    duration = endtime - starttime
    return render(request,template_name='updateitem.html',context={'duration':duration})
