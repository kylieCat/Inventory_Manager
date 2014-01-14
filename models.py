#Author: Ian Auld
#Date: '1/14/14'
#PyVer: 3.3
#Title: 'Inventory_Manager'
#Description:

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine


Base = declarative_base()


#region Shelf Class
class Shelf(Base):
    __tablename__ = 'shelf'
    shelf_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)
#endregion


#region Item Class
class Item(Base):
    __tablename__ = 'item'
    item_id = Column(Integer, primary_key=True, autoincrement=True)
    sku = Column(String(50), nullable=False, unique=True)
    title = Column(String(100), nullable=False)
#endregion


#region Bin Class
class Bin(Base):
    __tablename__ = 'bin'
    bin_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)
    shelf_id = Column(Integer, ForeignKey('shelf.shelf_id'))
#endregion


#region bin_item class
class BinItem(Base):
    __tablename__ = 'bin_item'
    bin_id = Column(Integer, ForeignKey('bin.bin_id'), primary_key=True)
    item_id = Column(Integer, ForeignKey('item.item_id'), primary_key=True)
    qty = Column(Integer, nullable=False)
#endregion

engine = create_engine('sqlite:///inventory.db')
Base.metadata.create_all(engine)