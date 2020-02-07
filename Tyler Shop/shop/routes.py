import os
from flask import render_template, url_for, request, redirect, flash, abort, Blueprint, session
from shop import app, db
from shop.models import Item, User
from shop.forms import RegistrationForm, LoginForm, CheckoutForm, ItemSearchForm
from flask_login import login_user, current_user, logout_user, login_required



@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    form = ItemSearchForm()
    search = ItemSearchForm(request.form)
    
    if request.method == 'POST':
        items = []
        search_string = search.data['search']
        if search.data['search'] == '':
            items = Item.query.all()
            return render_template('home.html', items=items, form=form)
        else:
            items = Item.query.filter(Item.item_name==search_string)
            return render_template('home.html', items=items, form=form)
        if not items:
            flash('No results found!')
            return redirect('/')
        else:
            return render_template('home.html', items=items, form=form)
        

    items = Item.query.all()
    return render_template('home.html', items=items, form=form)


@app.route("/Price high to low", methods=['GET', 'POST'])
def price_high_to_low():
    form = ItemSearchForm()
    search = ItemSearchForm(request.form)
    items = Item.query.order_by(Item.price)
    items = items[::-1]
    if request.method == 'POST':
        items = []
        search_string = search.data['search']
        if search.data['search'] == '':
            items = Item.query.all()
            return render_template('home.html', items=items, form=form)
        else:
            items = Item.query.filter(Item.item_name==search_string)
            return render_template('home.html', items=items, form=form)
        if not items:
            flash('No results found!')
            return redirect('/')
        else:
            return render_template('home.html', items=items, form=form)
        
    return render_template('home.html', items=items, form=form)

@app.route("/Price low to high", methods=['GET', 'POST'])
def price_low_to_high():
    form = ItemSearchForm()
    search = ItemSearchForm(request.form)
    items = Item.query.order_by(Item.price)
    if request.method == 'POST':
        items = []
        search_string = search.data['search']
        if search.data['search'] == '':
            items = Item.query.all()
            return render_template('home.html', items=items, form=form)
        else:
            items = Item.query.filter(Item.item_name==search_string)
            return render_template('home.html', items=items, form=form)
        if not items:
            flash('No results found!')
            return redirect('/')
        else:
            return render_template('home.html', items=items, form=form)
    return render_template('home.html', items=items, form=form)

@app.route("/Stock high to low", methods=['GET', 'POST'])
def stock_high_to_low():
    form = ItemSearchForm()
    search = ItemSearchForm(request.form)
    items = Item.query.order_by(Item.stock_level)
    items = items[::-1]
    if request.method == 'POST':
        items = []
        search_string = search.data['search']
        if search.data['search'] == '':
            items = Item.query.all()
            return render_template('home.html', items=items, form=form)
        else:
            items = Item.query.filter(Item.item_name==search_string)
            return render_template('home.html', items=items, form=form)
        if not items:
            flash('No results found!')
            return redirect('/')
        else:
            return render_template('home.html', items=items, form=form)
    return render_template('home.html', items=items, form=form)

@app.route("/Stock low to high", methods=['GET', 'POST'])
def stock_low_to_high():
    form = ItemSearchForm()
    search = ItemSearchForm(request.form)
    items = Item.query.order_by(Item.stock_level)
    if request.method == 'POST':
        items = []
        search_string = search.data['search']
        if search.data['search'] == '':
            items = Item.query.all()
            return render_template('home.html', items=items, form=form)
        else:
            items = Item.query.filter(Item.item_name==search_string)
            return render_template('home.html', items=items, form=form)
        if not items:
            flash('No results found!')
            return redirect('/')
        else:
            return render_template('home.html', items=items, form=form)
    return render_template('home.html', items=items, form=form)

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/item/<int:item_id>")
def item(item_id):
    item = Item.query.get_or_404(item_id)
    return render_template('item.html', title=item.item_name, item=item)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created. You can now log in.')
        return redirect(url_for('thankyou'))
    
    return render_template('register.html', title='Register', form=form)

@app.route("/thankyou")
def thankyou():
    return render_template('thankyou.html', title='Thankyou')

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return redirect(url_for('welcome'))
    return render_template('login.html', title='Login', form=form)

@app.route("/welcome")
def welcome():
    return render_template('welcome.html', title='Welcome')

@app.route("/logout")
def logout():
    logout_user()

    if "basket" in session:
        session["basket"].clear()
    if "wishlist" in session:
        session["wishlist"].clear()

    return render_template('logout.html', title='Welcome')
    


@app.route("/basket", methods=['GET', 'POST'])
def basket_display():
    if "basket" not in session:
        flash('There is nothing currently in your basket.')
        return render_template('basket.html', display_basket = {}, total =0)
    else:
        items = session['basket']
        basket = {}

        total_price = 0
        total_quantity = 0
        basket_total = 0
        for item in items:
            item = Item.query.get_or_404(item)
            total_price += item.price
            if item.id in basket:
                basket[item.id]["quantity"] += 1
            else:
                basket[item.id] = {"quantity":1, "name": item.item_name, "price": item.price, "image": item.image_file}
                
            total_quantity = sum(item['quantity'] for item in basket.values())

        return render_template("basket.html", title='Your Shopping Basket', display_basket = basket, total = total_price, total_quantity = total_quantity)
                
    return render_template('basket.html')

@app.route("/add_to_basket/<int:item_id>")
def add_to_basket(item_id):
    if item_id == 0:
        return redirect("/basket")
    else:
        if "basket" not in session:
            session["basket"] = []
        session["basket"].append(item_id)
        flash("Item added to your shopping basket")
        return redirect("/basket")

@app.route("/delete_item/<int:item_id>", methods=['POST'])
def delete_item(item_id):
    if "basket" not in session:
        session["basket"] = []
    session["basket"].remove(item_id)

    flash("The item has been removed from your shopping basket!")
    session.modified = True
    return redirect("/basket")

@app.route("/checkout", methods=['GET', 'POST'])
def checkout():
    form = CheckoutForm()
    if form.validate_on_submit():
        flash('Checkout has been successful.')
        return redirect(url_for('checkoutsuccessful'))
    return render_template('checkout.html', title='Checkout', form=form)

@app.route("/checkoutsuccess")
def checkoutsuccessful():
    session["basket"].clear()
    return render_template('checkoutsuccess.html')

@app.route('/results')
def show_results(items):
    return render_template('searchresults.html')


@app.route("/wishlist", methods=['GET', 'POST'])
def wishlist_display():
    if "wishlist" not in session:
        flash('There is nothing currently on your wishlist.')
        return render_template('wishlist.html', display_wishlist = {}, total =0)
    else:
        items = session['wishlist']
        wishlist = {}

        total_price = 0
        total_quantity = 0
        wishlist_total = 0
        for item in items:
            item = Item.query.get_or_404(item)
            total_price += item.price
            if item.id in wishlist:
                wishlist[item.id]["quantity"] += 1
            else:
                wishlist[item.id] = {"quantity":1, "name": item.item_name, "price": item.price, "image": item.image_file}
                
            total_quantity = sum(item['quantity'] for item in wishlist.values())

        return render_template("wishlist.html", title='Your Wishlist', display_wishlist = wishlist, total = total_price, total_quantity = total_quantity)
                
    return render_template('wishlist.html')

@app.route("/add_to_wishlist/<int:item_id>")
def add_to_wishlist(item_id):
    if item_id == 0:
        return redirect("/wishlist")
    else:
        if "wishlist" not in session:
            session["wishlist"] = []
        session["wishlist"].append(item_id)
        flash("Item added to your wishlist")
        return redirect("/wishlist")

@app.route("/delete_wishlist_item/<int:item_id>", methods=['POST'])
def delete_wishlist_item(item_id):
    if "wishlist" not in session:
        session["wishlist"] = []
    session["wishlist"].remove(item_id)

    flash("The item has been removed from your wishlist!")
    session.modified = True
    return redirect("/wishlist")



    
    



