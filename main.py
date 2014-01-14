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

db = 'inventory.sqlite'
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
        (cur, con) = open_db(db)
        cur.execute("INSERT into Items (sku, title) VALUES (?,?)", (n_sku, n_title))
        close_db(con)

    elif choice == 2:  # create bin
        n_name = input('Name >> ').upper()
        n_bin_shelf = input('What shelf will the bin be on >> ').upper()
        (cur, con) = open_db(db)
        cur.execute(
            "INSERT into Bins (name, shelf_id) VALUES (?,(SELECT shelf_id FROM Shelves WHERE name=?))",
            [n_name, n_bin_shelf]
        )
        close_db(con)

    elif choice == 3:  # create shelf
        n_name = input('Name >> ').upper()
        (cur, con) = open_db(db)
        cur.execute("INSERT into Shelves (name) VALUES (?)", [n_name])
        close_db(con)

    elif choice == 4:  # add item to bin
        in_bin = int(input('Enter the id of the bin you are adding to >> '))
        in_item = int(input('Enter the id of the item your adding to a bin >> '))
        in_qty = int(input('Enter the qty you are adding (Enter a negative to remove) >> '))
        (cur, con) = open_db(db)
        cur.execute("INSERT into Bin_Contents (bin_id, item_id, qty) VALUES (?,?,?)", (in_bin, in_item, in_qty))
        close_db(con)

    elif choice == 5:  # Display bin contents
        q_bin = input('What bin >> ').upper()
        (cur, con) = open_db(db)
        results = cur.execute(
            "SELECT \
            i.sku, \
            i.title, \
            bc.qty \
            FROM Items i \
            INNER JOIN Bin_Contents bc \
              on bc.item_id = i.item_id \
            INNER JOIN Bins b \
              on bc.bin_id = b.bin_id \
            WHERE b.name = ?", [q_bin]
        )
        response = results.fetchall()
        print(response)

    elif choice == 6:
        q_item = input('Enter the SKU of the item you\'re looking for >> ').upper()
        (cur, con) = open_db(db)
        results = cur.execute(
            "SELECT \
            i.sku, \
            i.title, \
            b.name, \
            bc.qty \
            FROM Items i \
            INNER JOIN Bin_Contents bc \
              on bc.item_id = i.item_id \
            INNER JOIN Bins b \
              on bc.bin_id = b.bin_id \
            WHERE i.sku = ?", [q_item]
        )
        response = results.fetchall()
        for row in response:
            print(row)
    elif choice == 9:
        exit(0)