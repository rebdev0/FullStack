from flask import Flask, flash, jsonify, redirect, render_template, request, url_for
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Set up the connection to the restaurant database
import sys
sys.path.append('database')
from restaurant_database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///database/restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# -----------------------------------------------------------
# Delete an item from a menu
# -----------------------------------------------------------
@app.route('/restaurants/<int:restaurant_id>/menu/<int:item_id>/delete', methods = ['GET', 'POST'])
def deleteMenuItem(restaurant_id, item_id):
	selectedRestaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	deleteItem = session.query(MenuItem).filter_by(id = item_id).one()
	if request.method == 'POST':
		session.delete(deleteItem)
		session.commit()
		flash("%s deleted successfully!" % deleteItem.name)
		return redirect(url_for('showMenu', restaurant_id = restaurant_id)) 
	else:
		return render_template('deleteMenuItem.html', item = deleteItem, restaurant = selectedRestaurant)

# -----------------------------------------------------------
# Delete a restaurant, which will also delete all menu items
# from the restaurant
# -----------------------------------------------------------
@app.route('/restaurants/<int:restaurant_id>/delete', methods = ['GET', 'POST'])
def deleteRestaurant(restaurant_id):
	deleteRestaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	if request.method == 'POST':
		session.delete(deleteRestaurant)
		session.commit()
		flash("%s deleted successfully!" % deleteRestaurant.name)
		return redirect(url_for('showRestaurants'))
	else:
		return render_template('deleteRestaurant.html', restaurant = deleteRestaurant)

# -----------------------------------------------------------
# Edit attributes of a menu item
# -----------------------------------------------------------	
@app.route('/restaurants/<int:restaurant_id>/menu/<int:item_id>/edit', methods = ['GET', 'POST'])
def editMenuItem(restaurant_id, item_id):
	selectedRestaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	editItem = session.query(MenuItem).filter_by(id = item_id).one()
	if request.method == 'POST':
		# Check for errors
		if not (request.form['name'] and request.form['price']):
			errors = ["Name and Price are required fields"]
			return render_template('editMenuItem.html', restaurant = selectedRestaurant, item = editItem, errors = errors)
		else:
			editItem.name = request.form['name']
			editItem.description = request.form['description']
			editItem.price = request.form['price']
			editItem.course = request.form['course']
			session.commit()
			flash("%s changed successfully!" % editItem.name)
			return redirect(url_for('showMenu', restaurant_id = restaurant_id))
	else:
		return render_template('editMenuItem.html', restaurant = selectedRestaurant, item = editItem)

# -----------------------------------------------------------
# Edit attributes of a restaurant
# -----------------------------------------------------------
@app.route('/restaurants/<int:restaurant_id>/edit', methods = ['GET', 'POST'])
def editRestaurant(restaurant_id):
	editRestaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	if request.method == 'POST':
		# Check for input errors
		if not request.form['name']:
			errors = ['Name is a required field']
			return render_template('editRestaurant.html', restaurant = editRestaurant, errors=errors)
		else:
			editRestaurant.name = request.form['name']
			editRestaurant.description = request.form['description']
			editRestaurant.address = request.form['address']
			editRestaurant.phone = request.form['phone']
			editRestaurant.website = request.form['website']
			session.commit()
			flash("%s changed successfully!" % editRestaurant.name)
			return redirect(url_for('showRestaurants'))
	else:
		return render_template('editRestaurant.html', restaurant = editRestaurant)

# -----------------------------------------------------------
# Add a new menu item to a restaurant
# -----------------------------------------------------------
@app.route('/restaurants/<int:restaurant_id>/menu/new', methods = ['GET', 'POST'])
def newMenuItem(restaurant_id):
	selectedRestaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	if request.method == 'POST':
		# Check for errors
		if not (request.form['name'] and request.form['price']):
			errors = ["Name and Price are required fields"]
			return render_template('newMenuItem.html', restaurant = selectedRestaurant, errors = errors)
		else:
			newMenuItem = MenuItem(name = request.form['name'], description = request.form['description'], price  = request.form['price'], course = request.form['course'], restaurant_id = restaurant_id)
			session.add(newMenuItem)
			session.commit()
			flash("%s added successfully!" % newMenuItem.name)
			return redirect(url_for('showMenu', restaurant_id = restaurant_id))
	else:
		return render_template('newMenuItem.html', restaurant = selectedRestaurant)

# -----------------------------------------------------------
# Add a new restaurant
# -----------------------------------------------------------
@app.route('/restaurants/new', methods = ['GET', 'POST'])
def newRestaurant():
	if request.method == 'POST':
		# Check for errors - name is a required field
		if not request.form['name']:
			errors = {'Name is a required field'}
			return render_template('newRestaurant.html', errors = errors)
		else:
			newRestaurant = Restaurant(name = request.form['name'], description = request.form['description'], address = request.form['address'], phone = request.form['phone'], website = request.form['website'])
			session.add(newRestaurant)
			session.commit()
			flash("%s added successfully!" % newRestaurant.name)
			return redirect(url_for('showRestaurants'))
	else:
		return render_template('newRestaurant.html')
	
# -----------------------------------------------------------
# Show the menu items for a restaurant
# -----------------------------------------------------------
@app.route('/restaurants/<int:restaurant_id>/menu')
@app.route('/restaurants/<int:restaurant_id>')
def showMenu(restaurant_id):
	selectedRestaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	allMenuItems = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
	return render_template('menu.html', restaurant = selectedRestaurant, items = allMenuItems)
	
# -----------------------------------------------------------
# Show all the restaurants
# -----------------------------------------------------------
@app.route('/restaurants')
@app.route('/')	
def showRestaurants():
	allRestaurants = session.query(Restaurant).all()
	return render_template('restaurants.html', restaurants = allRestaurants)

# -----------------------------------------------------------
# Get JSON object of all restaurants
# -----------------------------------------------------------
@app.route('/restaurants/JSON')
def getRestaurantsJSON():
	allRestaurants = session.query(Restaurant).all()
	return jsonify(Restaurants = [restaurant.serialize for restaurant in allRestaurants])
	
# -----------------------------------------------------------
# Get JSON object of all menu items for a specific restaurant
# -----------------------------------------------------------
@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def getMenuJSON(restaurant_id):
	allItems = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
	return jsonify(MenuItems = [item.serialize for item in allItems])
	
# -----------------------------------------------------------
# Get JSON object of specific menu item
# -----------------------------------------------------------
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/JSON')
def getMenuItemJSON(restaurant_id, menu_id):
	item = session.query(MenuItem).filter_by(id = menu_id).one()
	return jsonify(MenuItem = item.serialize)
	
if __name__ == '__main__':
	app.debug = True
	app.secret_key = "some secret key"
	app.run(host = '0.0.0.0', port = 5000)