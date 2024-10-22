from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route for the new page
@app.route('/new-page')
def new_page():
    return render_template('newpage.html')

# Route to handle login form submission
@app.route('/login', methods=['POST'])
def login():
    # For now, just redirect to the new page
    return redirect(url_for('new_page'))

# Route to handle registration form submission
@app.route('/register', methods=['POST'])
def register():
    # For now, just redirect to the new page
    return redirect(url_for('new_page'))

if __name__ == '__main__':
    app.run(debug=True)