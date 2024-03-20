from flask import Flask, render_template, request, redirect, session, g

users = [
    {'username': 'admin', 'password': '1111', 'role': 'admin'},
    {'username': 'john', 'password': '1111', 'role': 'user'},
    {'username': 'mary', 'password': '1111', 'role': 'user'},
]

app = Flask(__name__)
app.secret_key = 'adsasd867adshjasdaysdaisdasdyasydasdy7sdy8dys8a7y'
app.config['SESSION_TYPE'] = 'filesystem'


def find_current_user():
    username = session.get('username')
    if username is None:
        g.user = None
    else:
        for user in users:
            if user['username'] == username:
                g.user = user
                break


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        for user in users:
            if user['username'] == username and user['password'] == password:
                session['username'] = username
                return redirect('/dashboard')
        return render_template("login.html", error="Wrong credentials")
    else:
        return render_template("login.html", error="")

@app.route("/dashboard")
def dashboard():
    find_current_user()
    if g.user is None:
        return render_template("login.html", error="Login required")
    else:
        return render_template("dashboard.html", username=g.user['username'])
    
@app.route("/admin")
def admin():
    find_current_user()
    if g.user is None:
        return render_template("login.html", error="Login required")
    elif g.user['role'] == 'admin':
        return render_template("admin.html", username=g.user['username'])
    else:
        return render_template("login.html", error="Admin role required")
        
    
@app.route("/logout")
def logout():
    session.clear()
    return redirect('/')