import os
from flask import Flask, render_template, redirect, flash, session, request
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from forms import AddItemForm, NewUserForm, LoginForm
from models import db, connect_db, Item, Order, OrderItem, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = (os.environ.get('DATABASE_URL', 'postgres:///cart_test2'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = (os.environ.get('SECRET_KEY', 'secret'))
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def list_items():
    if 'user_id' in session:
        all_items = Item.query.all()
        username = session['user_id']
        print(f"""
              
              {username}
              {username}
              {username}
              {username}
              {username}
              
              """)
        curr_user = User.query.filter_by(username=username).first()
        cart = Order.query.filter_by(user_id=curr_user.id).filter_by(order_status='cart').first()
        return render_template('index.html', items=all_items, order=cart)
    else:
        return redirect('/signup')

@app.route('/signup', methods=['GET', 'POST'])
def signup_user():
    form = NewUserForm()
    
    if 'user_id' in session:
        flash("You are already signed up, and signed in. You've been redirected")
        return redirect('/')
        
    if form.validate_on_submit():
        new_user = User.register(form=form)
        db.session.add(new_user)
        
        try:
            db.session.commit()
        except IntegrityError:
            flash('oopsies')
            return redirect('/signup')
        
        reg_user = User.query.get_or_404(new_user.id)
        cart = Order(user_id=new_user.id)
        
        try:
            db.session.add(cart)
            db.session.commit()
        
        except IntegrityError:
            flash('There was an error signing you up. Please try again.')
            return redirect('/signup')
        
        session['user_id'] = new_user.username
        flash("Account created successfully")
        return redirect('/')
        
    return render_template('signup.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login_user():
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.authenticate(form=form)
        
        if user:
            flash(f"Welcome back, {user.username}.")
            session['user_id'] = user.username
            return redirect('/')
        
        else:
            form.username.errors = ["Invalid username or password."]
            
    if 'user_id' in session:
        return redirect('/')
    
    return render_template('login.html', form=form)

@app.route('/logout')
def logout_user():
    session.pop('user_id')
    flash("Goodbye!")
    return redirect('/login')

@app.route('/items/<int:item_id>/<int:order_id>/add', methods=["POST"])
def add_item_to_cart(item_id, order_id):
    #Grab quantity num from HTML form on previous page, if any,
    #and convert to integer
    quantity = int(request.form.get('quantity'))
    check_orders = OrderItem.query.filter(
        OrderItem.order_id == order_id).filter(
        OrderItem.item_id == item_id).first()
    ## todo: fix 
    if check_orders:
        check_orders.quantity += quantity
        db.session.commit()
        
    else:  
        item_to_add = OrderItem(
            item_id=item_id,
            order_id=order_id,
            quantity=quantity)
        db.session.add(item_to_add)
        db.session.commit()
    
    return redirect('/')
    
@app.route('/checkout/<int:order_id>', methods=['GET'])
def confirm_current_cart(order_id):
    cart = Order.query.get(order_id)
    items = cart.items
    price = sum([i.quantity * i.item.price for i in cart.items])
    return render_template('checkout.html', items=items, price=price, cart=cart)
    
@app.route('/checkout/<int:order_id>', methods=['POST'])
def send_order(order_id):
    cart = Order.query.get(order_id)
    cart.order_status = 'complete'
    
    username = session['user_id']
    curr_user = User.query.get_or_404(cart.user.id)
    
    new_cart = Order(user_id=curr_user.id)
    db.session.add(new_cart)
    try:
        db.session.commit()
        flash("Order complete, you have now been redirected home")
        return redirect('/')
    except IntegrityError:
        db.session.rollback()
        flash("Issue submitting your order. Try again.")
        return redirect(f'/checkout/{curr_user.id}')
    
@app.route('/users/<int:id>')
def user_page(id):
    if 'user_id' in session:
        target_user = User.query.get_or_404(id)
        curr_user = User.query.filter_by(
            username=session['user_id']
        ).first()
        if curr_user != target_user or 'user_id' not in session:
            return redirect('/')
        elif curr_user == target_user:
           
            orders = Order.query.filter_by(
                user_id=curr_user.id
            ).filter_by(
                order_status='complete'
            ).all()
            
            return render_template('user_page.html', user=curr_user, orders=orders)
    