from models import db, Item, Order, OrderItem, User
from random import randint
from app import app

db.drop_all()
db.create_all()

Item.query.delete()
Order.query.delete()
OrderItem.query.delete()
User.query.delete()

i1 = Item(name='eggs')
i2 = Item(name='milk')
i3 = Item(name='bread')

db.session.add_all([i1, i2, i3])
db.session.commit() 