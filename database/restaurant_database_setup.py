import sys
import os

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

#-----------------------------------------------------
# Class representing the restaurant table in the
# database. 
#-----------------------------------------------------
class Restaurant(Base):
	__tablename__ = 'restaurant'
	id = Column(Integer, primary_key = True)
	name = Column(String(80), nullable = False)
	description = Column(String(250), nullable = True)
	address = Column(String(300), nullable = True)
	phone = Column(String(25), nullable = True)
	website = Column(String(100), nullable = True)
	
#-----------------------------------------------------
# Class representing the menu item table in the
# database. 
#----------------------------------------------------	
class MenuItem(Base):
	__tablename__ = 'menu_item'
	id = Column(Integer, primary_key = True)
	name = Column(String(80), nullable = False)
	course = Column(String(250))
	description = Column(String(250))
	price = Column(String(8))
	restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
	restaurant = relationship(Restaurant)
	
	@property
	def serialize(self):
		return { 'name': self.name, 'description': self.description, 'id' : self.id, 'price' : self.price, 'course' : self.course }

#-----------------------------------------------------
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.create_all(engine)
