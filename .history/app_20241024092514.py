# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'
users = {}

class item():
    def __init__(self, _name, _description, _price, _priority) -> None:
        self.Name = _name
        self.Description = _description
        self.Price = _price
        self.Priority = _priority
    def getItemInfo(self):
        return [self.Name, self.Description, self.Price, self.Priority]
class preferences():
    def __init__(_color1, _color2, _color3, 
                 _shirtSize, _pantSizeLength, _pantSizeWidth,
                 _womensPantsSize, _shoeSize, _ringSize,
                 _jewleryMetalType) -> None:
        self.color1 = _color1
        preferences.color2 = _color2
        preferences.color3 = _color3
        preferences.shirtSize = _shirtSize
    def getItemInfo(self):
        return [self.Name, self.Description, self.Price, self.Priority]

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