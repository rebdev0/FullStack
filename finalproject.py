from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Set up the connection to the restaurant database
import sys
sys.path.append('database')
from restaurant_database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# ****************************************************************************************
# Temporary data for testing page functionality

# Fake Restaurants
# testRestaurant = {'name': 'The CRUDdy Crab', 'id': '1'}
testRestaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}, {'name':'Pizza Palace', 'id':'4'}]

# Fake Menu Items
testItems = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
# testItem =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree'}

# Fake Restaurant - Items table - numbers are indexes into testItems table - 0 -4
restaurantItems = [{0,2,4}, {1, 3}, {0,1,4}, {}]
# ****************************************************************************************

# -----------------------------------------------------------
# TODO - Delete an item from a menu
# -----------------------------------------------------------
@app.route('/restaurant/<int:restaurant_id>/menu/<int:item_id>/delete')
def deleteMenuItem(restaurant_id, item_id):
	return render_template('deleteMenuItem.html', item = testItems[item_id-1], restaurant = testRestaurants[restaurant_id-1])

# -----------------------------------------------------------
# TODO - Delete a restaurant, which will also delete all menu items
# from the restaurant
# -----------------------------------------------------------
@app.route('/restaurant/<int:restaurant_id>/delete')
def deleteRestaurant(restaurant_id):
	# selectedRestaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	return render_template('deleteRestaurant.html', restaurant = testRestaurants[restaurant_id-1])

# -----------------------------------------------------------
# TODO - Edit attributes of a menu item
# -----------------------------------------------------------	
@app.route('/restaurant/<int:restaurant_id>/menu/<int:item_id>/edit')
def editMenuItem(restaurant_id, item_id):
	return render_template('editMenuItem.html', restaurant = testRestaurants[restaurant_id-1], item = testItems[item_id-1])

# -----------------------------------------------------------
# TODO - Edit attributes of a restaurant
# -----------------------------------------------------------
@app.route('/restaurant/<int:restaurant_id>/edit')
def editRestaurant(restaurant_id):
	return render_template('editRestaurant.html', restaurant = testRestaurants[restaurant_id-1])

# -----------------------------------------------------------
# TODO - Add a new menu item to a restaurant
# -----------------------------------------------------------
@app.route('/restaurant/<int:restaurant_id>/menu/new')
def newMenuItem(restaurant_id):
	return render_template('newMenuItem.html', restaurant = testRestaurants[restaurant_id-1])

# -----------------------------------------------------------
# Add a new restaurant
# -----------------------------------------------------------
@app.route('/restaurant/new', methods = ['GET', 'POST'])
def newRestaurant():
	if request.method == 'POST':
		newRestaurant = Restaurant(name = request.form['name'], description = request.form['description'], address = request.form['address'], phone = request.form['phone'], website = request.form['website'])
		session.add(newRestaurant)
		session.commit()
		return redirect(url_for('showRestaurants'))
	else:
		return render_template('newRestaurant.html')
	
# -----------------------------------------------------------
# TODO - Show the menu items for a restaurant
# -----------------------------------------------------------
@app.route('/restaurant/<int:restaurant_id>/menu')
@app.route('/restaurant/<int:restaurant_id>')
def showMenu(restaurant_id):
	indices = restaurantItems[restaurant_id-1]
	menuItems = [testItems[index] for index in indices ]
	return render_template('menu.html', restaurant = testRestaurants[restaurant_id-1], items = menuItems)
	
# -----------------------------------------------------------
# Show all the restaurants
# -----------------------------------------------------------
@app.route('/restaurants')
@app.route('/')	
def showRestaurants():
	allRestaurants = session.query(Restaurant).all()
	return render_template('restaurants.html', restaurants = allRestaurants)

if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)