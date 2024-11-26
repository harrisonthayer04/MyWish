from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import db, User, Preferences, WishList, WishListItem
from werkzeug.security import generate_password_hash, check_password_hash



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wishlist_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'key'

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new-page')
def new_page():
    if 'user_email' not in session:
        flash('Please log in to access this page.')
        return redirect(url_for('index'))
    user = User.query.filter_by(email=session['user_email']).first()

    wishlist = WishList.query.filter_by(user_id=user.id, name='Default').first()
    if not wishlist:
        wishlist = WishList(name='Default', user_id=user.id)
        db.session.add(wishlist)
        db.session.commit()
    items = wishlist.items

    return render_template('new-page.html', user=user, items=items)
 
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    user = User.query.filter_by(email=email, password=password).first()
    if user:
        session['user_email'] = user.email
        flash('Logged in successfully!')
        return redirect(url_for('new_page'))
    else:
        flash('Invalid email or password. Please try again.')
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('user_email', None)
    flash('You have been logged out.')
    return redirect(url_for('index'))

@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

    if User.query.filter_by(email=email).first():
        flash('Email already registered. Please use a different email.')
        return redirect(url_for('index'))

    new_user = User(name=name, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
    flash('Registration successful! Please log in.')
    return redirect(url_for('index'))

@app.route('/preferences', methods=['GET', 'POST'])
def preferences():
    if 'user_email' not in session:
        flash('Please log in to set your preferences.')
        return redirect(url_for('index'))

    user = User.query.filter_by(email=session['user_email']).first()

    if request.method == 'POST':
        prefs = Preferences(
            color1=request.form['color1'],
            color2=request.form['color2'],
            color3=request.form['color3'],
            shirt_size=request.form['shirt_size'],
            pant_size_length=request.form['pant_size_length'],
            pant_size_width=request.form['pant_size_width'],
            womens_pants_size=request.form['womens_pants_size'],
            shoe_size=request.form['shoe_size'],
            ring_size=request.form['ring_size'],
            jewelry_metal_type=request.form['jewelry_metal_type'],
            user_id=user.id
        )
        db.session.add(prefs)
        db.session.commit()
        flash('Preferences saved!')
        return redirect(url_for('new_page'))

    return render_template('preferences.html')

@app.route('/add_item', methods=['POST'])
def add_item():
    if 'user_email' not in session:
        flash('Please log in to add items.')
        return redirect(url_for('index'))
    user = User.query.filter_by(email=session['user_email']).first()

    wishlist = WishList.query.filter_by(user_id=user.id, name='Default').first()
    if not wishlist:
        wishlist = WishList(name='Default', user_id=user.id)
        db.session.add(wishlist)
        db.session.commit()

 
    item_name = request.form['itemName']
    item_description = request.form.get('itemDescription')
    item_price = request.form.get('itemPrice')
    item_priority = request.form.get('itemPriority')

    priority_map = {'low': 1, 'medium': 2, 'high': 3}
    item_priority_value = priority_map.get(item_priority.lower(), 1)

    new_item = WishListItem(
        name=item_name,
        description=item_description,
        price=float(item_price) if item_price else None,
        priority=item_priority_value,
        wishlist_id=wishlist.id
    )
    db.session.add(new_item)
    db.session.commit()

    flash('Item added to your wishlist!')
    return redirect(url_for('new_page'))


if __name__ == '__main__':
    app.run(debug=True)