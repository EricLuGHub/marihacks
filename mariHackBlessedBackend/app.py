from flask import Flask
from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/your_database_name"
mongo = PyMongo(app)

@app.route('/test')
def hello_world():
    return 'Hello, World!'





if __name__ == '__main__':
    app.run(debug=True)