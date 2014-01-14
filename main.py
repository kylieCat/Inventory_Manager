#Author: Ian Auld
#Date: '1/6/14'
#PyVer: 3.3
#Title: 'Inventory_Manager'
#Description:


from sqlite3 import *
from models import *
from sqlalchemy.orm import sessionmaker


Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


#region Functions
def open_db(data):
    conn = connect(data)
    cursor = conn.cursor()
    return cursor, conn


def close_db(conn):
    conn.commit()
    conn.close()


def print_menu():
    print('1. Create item')
    print('2. Create bin')
    print('3. Create shelf')
    print('4. Add item to bin')
    print('5. Display bin contents')
    print('6. Display item and it\'s locations')
    print('9. Exit')
#endregion

db = 'inventory.db'
#region TABLE creation code
# (cur, con) = open_db(db)
# cur.execute("CREATE TABLE Items \
#             ( \
#                 item_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, \
#                 sku TEXT UNIQUE NOT NULL, \
#                 title TEXT UNIQUE NOT NULL \
#             )")
# close_db(con)
#
# (cur, con) = open_db(db)
# cur.execute("CREATE TABLE Bins \
#             ( \
#                 bin_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, \
#                 name TEXT NOT NULL, \
#                 shelf_id TEXT NOT NULL, \
#                 FOREIGN KEY (shelf_id) REFERENCES Shelves (shelf_id)  \
#             )")
# close_db(con)
#
# (cur, con) = open_db(db)
# cur.execute("CREATE TABLE Shelves \
#             ( \
#                 shelf_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, \
#                 name TEXT UNIQUE NOT NULL \
#             )")
# close_db(con)
#
# (cur, con) = open_db(db)
# cur.execute("CREATE TABLE Bin_Contents \
#             ( \
#                 bin_id INTEGER NOT NULL, \
#                 item_id INTEGER NOT NULL, \
#                 qty INTEGER NOT NULL, \
#                 CONSTRAINT PK_Bin_Contents PRIMARY KEY (bin_id, item_id), \
#                 FOREIGN KEY (bin_id) REFERENCES Bins (bin_id), \
#                 FOREIGN KEY (item_id) REFERENCES Items (item_id) \
#             )")
# close_db(con)
#
# (cur, con) = open_db(db)
# cur.execute("CREATE TABLE Shelf_Contents \
#             ( \
#                 shelf_id INTEGER NOT NULL, \
#                 bin_id INTEGER NOT NULL, \
#                 CONSTRAINT PK_Shelf_Contents PRIMARY KEY (shelf_id, bin_id), \
#                 FOREIGN KEY (shelf_id) REFERENCES Shelves (shelf_id), \
#                 FOREIGN KEY (bin_id) REFERENCES Bins (bin_id) \
#             )")
# close_db(con)
#endregion


while True:
    print_menu()
    choice = int(input('>> '))
    if choice == 1:  # create item
        n_sku = input('SKU >> ').upper()
        n_title = input('Title >> ')
        new_item = Item(sku=n_sku, title=n_title)
        session.add(new_item)
        session.commit()

    elif choice == 2:  # create bin
        n_name = input('Name >> ').upper()
        n_bin_shelf = input('What shelf will the bin be on >> ').upper()
        n_shelf_id = session.query(Shelf).filter(Shelf.name == n_bin_shelf).one()
        new_bin = Bin(name=n_name, shelf_id=n_shelf_id.shelf_id)
        session.add(new_bin)
        session.commit()

    elif choice == 3:  # create shelf
        n_name = input('Name >> ').upper()
        new_shelf = Shelf(name=n_name)
        session.add(new_shelf)
        session.commit()

    elif choice == 4:  # add item to bin
        in_bin = input('Bin name >> ')
        in_item = input('SKU >> ')
        in_qty = int(input('Enter the qty you are adding >> '))
        b = session.query(Bin).filter(Bin.name == in_bin).one()
        i = session.query(Item).filter(Item.sku == in_item).one()
        new_adjust = BinItem(bin_id=b.bin_id, item_id=i.item_id, qty=in_qty)
        session.add(new_adjust)
        session.commit()

    elif choice == 5:  # Display bin contents
        q_bin = input('What bin >> ').upper()
        results = session.query(BinItem, Item, Bin).\
            join(Item, BinItem.item_id == Item.item_id).\
            join(Bin, BinItem.bin_id == Bin.bin_id).\
            filter(Bin.name == q_bin)
        for row in results:
            print(row[1].sku, row[1].title, row[0].qty)

    elif choice == 6:  # Item and it's locations
        q_item = input('Enter the SKU of the item you\'re looking for >> ').upper()
        results = session.query(BinItem, Item, Bin).\
            join(Item, BinItem.item_id == Item.item_id).\
            join(Bin, BinItem.bin_id == Bin.bin_id).\
            filter(Item.sku == q_item)
        for row in results:
            print(row[1].sku, row[1].title, row[2].name, row[0].qty)
    elif choice == 9:
        exit(0)