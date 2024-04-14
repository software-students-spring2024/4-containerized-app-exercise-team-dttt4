from flask import Flask, request, render_template
from pymongo import MongoClient
from PIL import Image 
import io
from bson import binary 


app = Flask(__name__)


# connect to MongoDB server
client = MongoClient('localhost', 27017)
db = client['sample_mflix']
collection = db['images']

# # get database
# db = client.test

@app.route('/', methods=['GET', 'POST'])
def process_image():

    return render_template('process_image.html')
    #return "<h1>Test</h1>"



if __name__ == '__main__':
    app.run(debug=True)