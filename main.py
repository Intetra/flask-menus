from flask import Flask, render_template, request, redirect
from flask import jsonify, flash, url_for
app = Flask(__name__)


import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
engine = create_engine('postgresql:///restaurantmenu')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
def menusFront():
    restaurants = session.query(Restaurant).all()
    return render_template('menusfront.html', restaurants=restaurants)


@app.route('/menus/restaurant/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id)
    return render_template('menu.html', restaurant=restaurant, items=items)


@app.route('/menus/restaurant/<int:restaurant_id>/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'],
                           price=request.form['price'],
                           description=request.form['description'],
                           restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        flash("New menu item created!")
        return redirect(url_for('restaurantMenu',
                                restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)


@app.route('/menus/restaurant/<int:restaurant_id>/<int:menu_id>/edit/',
           methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    x = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        x.name = name
        x.price = price
        x.description = description
        session.commit()
        flash("Menu item edited!")
        return redirect(url_for('restaurantMenu',
                                restaurant_id=restaurant_id))
    else:
        return render_template('editmenuitem.html',
                               restaurant_id=restaurant_id,
                               menu_id=menu_id,
                               n=x.name,
                               p=x.price,
                               d=x.description)


@app.route('/menus/restaurant/<int:restaurant_id>/<int:menu_id>/delete/',
           methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    x = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(x)
        session.commit()
        flash("Menu item deleted!")
        return redirect(url_for('restaurantMenu',
                                restaurant_id=restaurant_id))
    else:
        return render_template('deletemenuitem.html',
                               restaurant_id=restaurant_id,
                               menu_id=menu_id,
                               x=x.name)


@app.route('/menus/restaurant/new', methods=['GET', 'POST'])
def newRestaurant():
    if request.method == 'POST':
        n = Restaurant(name=request.form['name'], description=request.form['description'])
        session.add(n)
        session.commit()
        flash("New restaurant created!")
        return redirect(url_for("menusFront"))
    else:
        return render_template('newrestaurant.html')


@app.route('/menus/restaurant/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    x = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        session.delete(x)
        session.commit()
        flash("Restaurant deleted!")
        return redirect(url_for("menusFront"))
    else:
        return render_template('deleterestaurant.html',
                               restaurant_id=restaurant_id,
                               x=x.name)


@app.route('/menus/restaurant/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    x = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        n = request.form['name']
        n2 = request.form['description']
        x.name = n
        x.description = n2
        session.commit()
        flash("Restaurant edited!")
        return redirect(url_for("menusFront"))
    else:
        return render_template('editrestaurant.html',
                               restaurant_id=restaurant_id,
                               x=x.name,
                               y=x.description)

@app.route('/menus/restaurant/JSON/')
def restaurantsJSON():
    restaurants = session.query(Restaurant).all()
    return jsonify(Restaurants = [r.serialize for r in restaurants])


@app.route('/menus/restaurant/<int:restaurant_id>/menu/JSON/')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return jsonify(menuItems=[i.serialize for i in items])

@app.route('/menus/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON/')
def menuItemJSON(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(restaurant_id=restaurant_id, id=menu_id).one()
    return jsonify(Menu_Item = item.serialize)


if __name__ == '__main__':
    app.debug = False
    app.run(host='0.0.0.0', port=5000)
