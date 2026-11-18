from flask import Flask, render_template
from pymongo import MongoClient
import urllib.parse
import certifi

app = Flask(__name__)

username = "aindiramanayake_db_user"
password = urllib.parse.quote_plus("aLGh%y$ZmZt6rsX")

client = MongoClient(
    f"mongodb+srv://{username}:{password}@cluster0.t4htdp7.mongodb.net/",
    tlsCAFile=certifi.where()
)
db = client["3tier_db"]
logs_collection = db["visit_logs"]

@app.route('/')
def index():
    logs_collection.insert_one({"action": "Page loaded"})
    return render_template('presentation.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)