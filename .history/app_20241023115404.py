# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'
users = {}
class item():
    def __int__() -> None:
        item.Name = ""
        item.Description = ""
        item.Price = 0.0
        item.Pr

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new-page')
def new_page():
    if 'user_email' not in session:
        flash('Please log in to access this page.')
        return redirect(url_for('index'))
    return render_template('new-page.html')
 
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    
    if email in users and users[email]['password'] == password: 
        session['user_email'] = email
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