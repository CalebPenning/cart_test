from datetime import datetime
from random import randint
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)
    
class User(db.Model):
    """User instance. testing..."""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer,
                   primary_key=True,
                   unique=True,
                   nullable=False)
    
    username = db.Column(db.Text,
                         unique=True,
                         nullable=False)
    
    password = db.Column(db.Text,
                         nullable=False)

    email = db.Column(db.Text,
                      nullable=False,
                      unique=True)
    
    first_name = db.Column(db.Text,
                           nullable=False,
                           default="")
    
    last_name = db.Column(db.Text,
                          nullable=False,
                          default="")
    
    orders = db.relationship('Order',
                             backref='user')
    
    def __repr__(self):
        u = self
        return f"<User: {u.username}, Email: {u.email}, Name: {u.first_name} {u.last_name}>"

    @classmethod
    def register(cls, form):
        username = form.username.data
        password = form.username.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        
        hashed = bcrypt.generate_password_hash(password)
        
        hashed_utf8 = hashed.decode("utf8")
        
        return cls(username=username,
                   password=hashed_utf8,
                   email=email,
                   first_name=first_name,
                   last_name=last_name)
        
    @classmethod
    def authenticate(cls, form):
        u = User.query.filter_by(username=username).first()
        pwd = form.password.data
        
        if u and bcrypt.check_password_hash(u.password, pwd):
            return u
        else:
            return False
        
    
class Item(db.Model):
    __tablename__ = 'items'
    
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    
    name = db.Column(
        db.String(20),
        nullable=False
    )
    
    price = db.Column(
        db.Integer,
        nullable=False,
        default=randint(0, 20)
    )
    
    cart_additions = db.relationship(
        'OrderItem',
        backref='item'
    )

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    
    item_id = db.Column(
        db.Integer,
        db.ForeignKey('items.id'),
        primary_key=True
    )
    
    order_id = db.Column(
        db.Integer,
        db.ForeignKey('orders.id'),
        primary_key=True
    )
    
    quantity = db.Column(
        db.Integer,
        nullable=False
    )

class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    
    order_status = db.Column(
        db.String(20),
        nullable=False,
        default="cart"
    )
    
    items = db.relationship(
        'OrderItem',
        backref='order'
    )
    
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id')
    )
    
    