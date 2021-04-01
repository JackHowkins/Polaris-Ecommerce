from app import db

orders = db.Table('orders', db.Model.metadata,
    db.Column('productid', db.Integer, db.ForeignKey('products.productid'), primary_key=True),
    db.Column('customerid', db.Integer, db.ForeignKey('customers.customerid'), primary_key=True),
)

class Products(db.Model):
    productid = db.Column(db.Integer, primary_key=True)
    productname = db.Column(db.String(75))
    price = db.Column(db.String(6))
    image = db.Column(db.String(50))
    category = db.Column(db.String(50))
    range = db.Column(db.String(50))
    description = db.Column(db.String(5000))
    xsstocklevel = db.Column(db.Integer)
    sstocklevel = db.Column(db.Integer)
    mstocklevel = db.Column(db.Integer)
    lstocklevel = db.Column(db.Integer)
    xlstocklevel = db.Column(db.Integer)
    soldhistory = db.Column(db.Integer)
    buyers = db.relationship('Customers',secondary=orders)

class Customers(db.Model):
    customerid = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(35))
    surname = db.Column(db.String(35))
    email = db.Column(db.String(75))
    password = db.Column(db.String(25))
    purchases = db.relationship('Products',secondary=orders)
