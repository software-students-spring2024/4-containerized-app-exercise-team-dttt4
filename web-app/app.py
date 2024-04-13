from flask import Flask, request
from markupsafe import escape
from pymongo import MongoClient


app = Flask(__name__)


# connect to MongoDB server
client = MongoClient('localhost', 27017)

# get database
db = client.test

@app.route('/index', method=['POST'])
def get_image();
    # get image for processing
    data = request.json

    # put data inside mongoDB 


if __name__ == '__main__':
    app.run()