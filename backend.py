from flask import Flask, render_template, request

app = Flask(__name__)

# Route for the home page
@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <title>MyWish</title>
        <style>
            @font-face {font-family: 'MyWishFont'; src:url('/static/fonts/MRFLemonberrySans.otf') format('opentype');}
            h1 {background-color: rgb(161, 113, 136); color: rgb(0, 0, 0); -webkit-text-stroke-width: 0px;
                -webkit-text-stroke-color: brown; text-align: center; font-size: 100px; font-family: 'MyWishFont';}
            body {background-color: rgb(161, 113, 136);}
            h2 {font-family: 'MyWishFont';}
            .container {display: flex; justify-content: center; align-items: center; flex-direction: row; gap: 100px;}
            .form-container {background-color: white; padding: 20px; margin: 10px; border: 1px solid #ccc;
                             border-radius: 8px; width: 300px; text-align: center;}
            input[type="text"], input[type="password"], input[type="email"] {width: 75%; padding: 10px; margin: 10px 0;
                                                                            border: 1px solid #ccc; border-radius: 4px;}
            input[type="submit"] {background-color: rgb(255,255,255); color: rgb(0, 0, 0); padding: 10px 20px;
                                  border-radius: 4px; cursor: pointer;}
            input[type="submit"]:hover {background-color: rgb(255,255,255);}
        </style>
    </head>
    <body>
        <a href="/about">
            <button>About</button>
        </a>
        <h1>Welcome to MyWish</h1>
        <div class="container">
            <div class="form-container">
                <h2>Login</h2>
                <form action="/login" method="POST">
                    <input type="text" name="username" placeholder="Username" required><br>
                    <input type="password" name="password" placeholder="Password" required><br>
                    <input type="submit" value="Login">
                </form>
            </div>
            <div class="form-container">
                <h2>Create Account</h2>
                <form action="/register" method="POST">
                    <input type="text" name="username" placeholder="Username" required><br>
                    <input type="email" name="email" placeholder="Email" required><br>
                    <input type="password" name="password" placeholder="Password" required><br>
                    <input type="submit" value="Create Account">
                </form>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/about')
def about():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <title>About MyWish</title>
        <style>
            @font-face {font-family: 'MyWishFont'; src:url('/static/fonts/MRFLemonberrySans.otf') format('opentype');}
            body {background-color: rgb(161, 113, 136); font-family: , sans-serif; text-align: center; color: white;}
            h1 {background-color: rgb(161, 113, 136); color: rgb(0, 0, 0); -webkit-text-stroke-width: 0px;
                -webkit-text-stroke-color: brown; text-align: center; font-size: 100px; font-family: 'MyWishFont';}
            body {background-color: rgb(161, 113, 136);}
            p {font-size: 24px;}
        </style>
    </head>
    <body>
        <h1>About MyWish</h1>
        <p>MyWish is a website that helps you give and receive more personal gifts!</p>
        <a href="/">Go Back Home</a>
    </body>
    </html>
    '''

# Route for login form (not functional yet)
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    return f'Login page. Username: {username}, Password: {password}'

# Route for registration form (not functional yet)
@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    return f'Register page. Username: {username}, Email: {email}, Password: {password}'

if __name__ == '__main__':
    app.run(debug=True)