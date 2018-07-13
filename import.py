from __future__ import unicode_literals
import pyodbc
import sqlite3 as db
import datetime


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

    #cursor2.execute("""Select QuickbookListID from pricequotation_pricelevel""")

    cursor2.close()
    cn2.close()
    return pricelevels_quickbooklistIDs


def getpricelevelperitem(items_quickbooklistIDs, pricelevels_quickbooklistIDs):
    cn1 = pyodbc.connect('DSN=QuickBooks Data;')
    cursor1 = cn1.cursor()

    db_filename = 'db.sqlite3'
    cn2 = db.connect(db_filename)
    cursor2 = cn2.cursor()

    cursor1.execute("""SELECT A.ListID ItemID, A.Name, A.FullName, A.SalesDesc, B.ListID PriceLevelListID, B.Name PriceLevelName, B.PriceLevelPerItemCustomPrice
FROM ItemInventoryAssembly A INNER JOIN PriceLevelPerItem B ON A.ListID = B.PriceLevelPerItemItemRefListID WHERE A.ListID IN %s AND B.ListID IN %s""" % (
    str(items_quickbooklistIDs), str(pricelevels_quickbooklistIDs)))

    params = []
    params = list((str(row.Name), str(row.FullName), str(row.SalesDesc), str(row.ItemID), str(row.PriceLevelName),
                   str(row.PriceLevelListID), float(row.PriceLevelPerItemCustomPrice)) for row in cursor1.fetchall())

    cursor2.execute("Delete FROM pricequotation_joinpricelevelperitem")
    cn2.commit()

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
    cn2.commit()

    cursor2.executemany(
        """INSERT INTO pricequotation_pricelevelperitem (item_id, pricelevel_id, customprice) VALUES (?,?,?)""", params)
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


    cursor1.execute("SELECT ListID, SalesPrice, SalesDesc FROM ItemInventoryAssembly WHERE ListID IN %s" %str(listid))

    itemlist = tuple((float(row.SalesPrice), str(row.SalesDesc), str(row.ListID)) for row in cursor1.fetchall())

    cursor2.executemany("UPDATE pricequotation_item SET salesprice = ?, description = ? WHERE QuickbookListID = ?",
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

print (endtime - starttime)


