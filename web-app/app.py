"""
This module contains a Flask web application that processes images.
"""
from flask import Flask, render_template
from pymongo import MongoClient


app = Flask(__name__)

# connect to MongoDB server
client = MongoClient('localhost', 27017)
db = client['sample_mflix']
collection = db['images']

@app.route('/', methods=['GET', 'POST'])
def process_image():
    """
    Open the landing page for image uploading
    """
    return render_template('process_image.html')



if __name__ == '__main__':
    app.run(debug=True)