from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    preferences = db.relationship('Preferences', uselist=False, backref='user')
    wishlists = db.relationship('WishList', backref='user', lazy=True)
    share_token = db.Column(db.String(64), unique=True, nullable)

class Preferences(db.Model):
    __tablename__ = 'preferences'
    id = db.Column(db.Integer, primary_key=True)
    color1 = db.Column(db.String(20))
    color2 = db.Column(db.String(20))
    color3 = db.Column(db.String(20))
    shirt_size = db.Column(db.String(5))
    pant_size_length = db.Column(db.Integer)
    pant_size_width = db.Column(db.Integer)
    womens_pants_size = db.Column(db.String(5))
    shoe_size = db.Column(db.Float)
    ring_size = db.Column(db.Float)
    jewelry_metal_type = db.Column(db.String(30))
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

class WishList(db.Model):
    __tablename__ = 'wishlists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    items = db.relationship('WishListItem', backref='wishlist', lazy=True)

class WishListItem(db.Model):
    __tablename__ = 'wishlist_items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    price = db.Column(db.Float)
    priority = db.Column(db.Integer)
    wishlist_id = db.Column(db.Integer, db.ForeignKey('wishlists.id'), nullable=False)


    