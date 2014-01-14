#Author: Ian Auld
#Date: '1/6/14'
#PyVer: 3.3
#Title: 'Inventory_Manager'
#Description:


from models import *
from sqlalchemy.orm import sessionmaker


Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


#region Functions
def print_menu():
    print('1. Create item')
    print('2. Create bin')
    print('3. Create shelf')
    print('4. Add item to bin')
    print('5. Display bin contents')
    print('6. Display item and it\'s locations')
    print('7. Take item from stock')
    print('0. Exit')


def add_record(obj):
    session.add(obj)
    session.commit()


def add_item(sku, title):
    new_item = Item(sku=sku, title=title)
    add_record(new_item)


def add_bin(name, s_name):
    # Finds shelf object that has a name matching the name entered by the user
    # This object is used to add the shelf_id to the new bin record
    s = session.query(Shelf).filter(Shelf.name == s_name).one()
    new_bin = Bin(name=name, shelf_id=s.shelf_id)
    add_record(new_bin)


def add_shelf(name):
    new_shelf = Shelf(name=name)
    add_record(new_shelf)
    session.commit()


def add_item_to_bin(b_name, i_sku, qty):
    b = session.query(Bin).filter(Bin.name == b_name).one()
    i = session.query(Item).filter(Item.sku == i_sku).one()
    new_adjust = BinItem(bin_id=b.bin_id, item_id=i.item_id, qty=qty)
    add_record(new_adjust)


def display_bin_contents(b_name):
    qry = session.query(BinItem, Item, Bin).\
        join(Item, BinItem.item_id == Item.item_id).\
        join(Bin, BinItem.bin_id == Bin.bin_id).\
        filter(Bin.name == b_name)
    return qry


def display_item_locations(i_sku):
    qry = session.query(BinItem, Item, Bin).\
        join(Item, BinItem.item_id == Item.item_id).\
        join(Bin, BinItem.bin_id == Bin.bin_id).\
        filter(Item.sku == i_sku)
    return qry
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
        add_item(n_sku, n_title)

    elif choice == 2:  # create bin
        n_name = input('Name >> ').upper()
        shelf_name = input('What shelf will the bin be on >> ').upper()
        add_bin(n_name, shelf_name)

    elif choice == 3:  # create shelf
        n_name = input('Name >> ').upper()
        add_shelf(n_name)

    elif choice == 4:  # add item to bin
        in_bin = input('Bin name >> ')
        in_item = input('SKU >> ')
        in_qty = int(input('Enter the qty you are adding >> '))
        add_item_to_bin(in_bin, in_item, in_qty)

    elif choice == 5:  # Display bin contents
        q_bin = input('What bin >> ').upper()
        results = display_bin_contents(q_bin)
        for row in results:
            print(row[1].sku, row[1].title, row[0].qty)

    elif choice == 6:  # Item and it's locations
        q_item = input('Enter the SKU of the item you\'re looking for >> ').upper()
        results = display_item_locations(q_item)
        for row in results:
            print(row[1].sku, row[1].title, row[2].name, row[0].qty)

    elif choice == 7:
        pass
    elif choice == 0:
        exit(0)