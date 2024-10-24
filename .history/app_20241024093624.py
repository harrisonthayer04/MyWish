# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import db, User, Preferences, WishList, WishListItem



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
    return render_template('new-page.html', user=user)
 
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
    # print(name, email, password) ~> useful for debugging
    if email in users:
        flash('Email already registered. Please use a different email.')
        return redirect(url_for('index'))
    
    users[email] = {'name': name, 'password': password}
    flash('Registration successful! Please log in.')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)