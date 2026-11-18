from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
import urllib.parse
import certifi
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.secret_key = 'super_secret_development_key' 

username = "aindiramanayake_db_user"
password = urllib.parse.quote_plus("aLGh%y$ZmZt6rsX")

client = MongoClient(
    f"mongodb+srv://{username}:{password}@cluster0.t4htdp7.mongodb.net/",
    tlsCAFile=certifi.where()
)
db = client["3tier_db"]
logs_collection = db["visit_logs"]
users_collection = db["users"] 

if not users_collection.find_one({"username": "admin"}):
    users_collection.insert_one({
        "username": "admin",
        "password": generate_password_hash("password123") 
    })

@app.route('/')
def index():
    if 'username' in session:
        logs_collection.insert_one({"action": f"Page loaded by {session['username']}"})
        return render_template('index.html', username=session['username'])
    
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        form_username = request.form['username']
        form_password = request.form['password']
        
        user = users_collection.find_one({"username": form_username})
        
        if user and check_password_hash(user['password'], form_password):
            session['username'] = form_username 
            return redirect(url_for('index'))
        else:
            error = "Invalid username or password"
            
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)