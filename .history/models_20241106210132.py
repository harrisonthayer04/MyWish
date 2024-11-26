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

@app.route('/preferences', methods=['GET', 'POST'])
def preferences():
    if 'user_email' not in session:
        flash('Please log in to set your preferences.')
        return redirect(url_for('index'))

    user = User.query.filter_by(email=session['user_email']).first()

    if request.method == 'POST':
        # Handle form submission
        # ... (handle preferences data and save to DB)
        flash('Preferences saved!')
        return redirect(url_for('new_page'))
    else:
        # GET method - pre-populate form if preferences exist
        existing_prefs = Preferences.query.filter_by(user_id=user.id).first()
        return render_template('new-page.html', preferences=existing_prefs, user=user)

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


    