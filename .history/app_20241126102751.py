from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import db, User, Preferences, WishList, WishListItem
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wishlist_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'key'

db.init_app(app)

@app.route('/change_name', methods=['POST'])
def change_name():
    if 'user_email' not in session:
        flash('Please log in to change your name.')
        return redirect(url_for('index'))

    user = User.query.filter_by(email=session['user_email']).first()
    new_name = request.form['newName'].strip()

    if not new_name:
        flash('Name cannot be empty.')
        return redirect(url_for('account'))
    if len(new_name) > 50:
        flash('Name is too long. Please limit to 50 characters.')
        return redirect(url_for('account'))
    user.name = new_name
    db.session.commit()
    flash('Your name has been updated.')
    return redirect(url_for('account'))

@app.route('/share/<share_token>')
def share_page(share_token):
    user = User.query.filter_by(share_token=share_token).first_or_404()

    wishlist = WishList.query.filter_by(user_id=user.id, name='Default').first()
    items = wishlist.items if wishlist else []
    preferences = Preferences.query.filter_by(user_id=user.id).first()

    return render_template('share_page.html', user=user, items=items, preferences=preferences)

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

    if not user.share_token:
        user.share_token = uuid.uuid4().hex
        db.session.commit()

    wishlist = WishList.query.filter_by(user_id=user.id, name='Default').first()
    if not wishlist:
        wishlist = WishList(name='Default', user_id=user.id)
        db.session.add(wishlist)
        db.session.commit()
    items = wishlist.items

    # Retrieve the user's preferences
    preferences = Preferences.query.filter_by(user_id=user.id).first()

    return render_template('new-page.html', user=user, items=items, preferences=preferences)

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


@app.route('/preferences', methods=['POST'])
def preferences():
    if 'user_email' not in session:
        flash('Please log in to set your preferences.')
        return redirect(url_for('index'))

    user = User.query.filter_by(email=session['user_email']).first()

    # Check if preferences already exist
    prefs = Preferences.query.filter_by(user_id=user.id).first()
    if not prefs:
        prefs = Preferences(user_id=user.id)
        db.session.add(prefs)

    # Update the preferences fields
    prefs.color1 = request.form['color1']
    prefs.color2 = request.form['color2']
    prefs.color3 = request.form['color3']
    prefs.shirt_size = request.form['shirt_size']
    prefs.pant_size_length = request.form['pant_size_length']
    prefs.pant_size_width = request.form['pant_size_width']
    prefs.womens_pants_size = request.form['womens_pants_size']
    prefs.shoe_size = request.form['shoe_size']
    prefs.ring_size = request.form['ring_size']
    prefs.jewelry_metal_type = request.form['jewelry_metal_type']

    db.session.commit()
    flash('Preferences saved!')
    return redirect(url_for('new_page'))

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

@app.route('/account', methods=['GET'])
def account():
    if 'user_email' not in session:
        flash('Please log in to access account settings.')
        return redirect(url_for('index'))
    return render_template('account.html')

@app.route('/change_password', methods=['POST'])
def change_password():
    if 'user_email' not in session:
        flash('Please log in to change your password.')
        return redirect(url_for('index'))

    user = User.query.filter_by(email=session['user_email']).first()

    current_password = request.form['currentPassword']
    new_password = request.form['newPassword']
    confirm_new_password = request.form['confirmNewPassword']

    if user.password != current_password:
        flash('Current password is incorrect.')
        return redirect(url_for('account'))

    if new_password != confirm_new_password:
        flash('New passwords do not match.')
        return redirect(url_for('account'))

    user.password = new_password
    db.session.commit()
    flash('Your password has been updated.')
    return redirect(url_for('account'))

@app.route('/delete_account', methods=['POST'])
def delete_account():
    if 'user_email' not in session:
        flash('Please log in to delete your account.')
        return redirect(url_for('index'))

    user = User.query.filter_by(email=session['user_email']).first()

    confirm_password = request.form['confirmPassword']

    if user.password != confirm_password:
        flash('Password is incorrect.')
        return redirect(url_for('account'))

    # Delete related data: preferences, wishlists, and wishlist items
    if user.preferences:
        db.session.delete(user.preferences)
    wishlists = WishList.query.filter_by(user_id=user.id).all()
    for wishlist in wishlists:
        for item in wishlist.items:
            db.session.delete(item)
        db.session.delete(wishlist)
    db.session.delete(user)
    db.session.commit()

    # Remove user from session
    session.pop('user_email', None)
    flash('Your account has been deleted.')
    return redirect(url_for('index'))

@app.route('/delete_item', methods=['POST'])
def delete_item():
    if 'user_email' not in session:
        flash('Please log in to delete items.')
        return redirect(url_for('index'))
    
    user = User.query.filter_by(email=session['user_email']).first()
    item_id = request.form.get('item_id')

    if not item_id:
        flash('Invalid item.')
        return redirect(url_for('new_page'))
    item = WishListItem.query.get(item_id)
    if not item:
        flash('Item not found.')
        return redirect(url_for('new_page'))
    if item.wishlist.user_id != user.id:
        flash('You are not authorized to delete this item.')
        return redirect(url_for('new_page'))
    db.session.delete(item)
    db.session.commit()
    flash('Item removed from your wishlist.')
    return redirect(url_for('new_page'))

if __name__ == '__main__':
    app.run(debug=True)