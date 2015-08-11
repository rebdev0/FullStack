from flask import Flask
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import sys
sys.path.append('database')
from restaurant_database_setup import Base, Restaurant, MenuItem
	
# from restaurant_database_setup import Base, Restaurant, MenuItem

### Connect to database
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# -----------------------------------------------------------
# Delete an item from a menu
# -----------------------------------------------------------
@app.route('/restaurant/<int:restaurant_id>/menu/<int:item_id>/delete')
def deleteMenuItem(restaurant_id, item_id):
	return "This page will be for deleting item %s" % item_id

# -----------------------------------------------------------
# Delete a restaurant, which will also delete all menu items
# from the restaurant
# -----------------------------------------------------------
@app.route('/restaurant/<int:restaurant_id>/delete')
def deleteRestaurant(restaurant_id):
	return "This page will be for deleting restaurant %s" % restaurant_id

# -----------------------------------------------------------
# Edit attributes of a menu item
# -----------------------------------------------------------	
@app.route('/restaurant/<int:restaurant_id>/menu/<int:item_id>/edit')
def editMenuItem(restaurant_id, item_id):
	return "This page is for editing menu item %s" % item_id

# -----------------------------------------------------------
# Edit attributes of a restaurant
# -----------------------------------------------------------
@app.route('/restaurant/<int:restaurant_id>/edit')
def editRestaurant(restaurant_id):
	return "This page will be for editing restaurant %s" % restaurant_id

# -----------------------------------------------------------
# Add a new menu item to a restaurant
# -----------------------------------------------------------
@app.route('/restaurant/<int:restaurant_id>/menu/new')
def newMenuItem(restaurant_id):
	return "This page is for making a new menu item for restaurant %s" % restaurant_id

# -----------------------------------------------------------
# Add a new restaurant
# -----------------------------------------------------------
@app.route('/restaurant/new')
def newRestaurants():
	return "This page will be for making a new restaurant"

# -----------------------------------------------------------
# Show the menu items for a restaurant
# -----------------------------------------------------------
@app.route('/restaurant/<int:restaurant_id>/menu')
@app.route('/restaurant/<int:restaurant_id>')
def showMenu(restaurant_id):
	return "This page is the menu for %s" % restaurant_id

# -----------------------------------------------------------
# Show all the restaurants
# -----------------------------------------------------------
@app.route('/restaurants')
@app.route('/')	
def showRestaurants():
	return "This page will show all my restaurants"
	
if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)