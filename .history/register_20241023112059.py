from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

users = {}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    users[email] = {'name': name, 'password': password}
    return redirect('/')

numberOfLogins = 0
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    if email in users and users[email]['password'] == password:
        with open('user_credentials.txt', 'a') as f:
            numberOfLogins += 1
            f.write(f'Email: {email}, Password: {password}\n')
        session['user_email'] = email
        return redirect('/main')
    else:
        flash('Invalid login credentials. Please try again.')
        return redirect('/')

