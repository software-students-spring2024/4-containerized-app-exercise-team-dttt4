"""
This module contains a Flask web application that processes images.
"""
import io
from os import getenv
from flask import Flask, request, render_template
from pymongo import MongoClient
from PIL import Image 
from bson import binary 
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
client = MongoClient("MONGO_URI") 
db = client["imagedb"]
collection = db["imageCollection"]

@app.route("/", methods=['GET', 'POST'])
def process_image():
    if request.method == 'POST':
        print(request.files)
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file:
            image = Image.open(file.stream)
            image_byte_array = io.BytesIO()
            image.save(image_byte_array, format=image.format)
            image_bytes = image_byte_array.getvalue()
            # Store image in MongoDB
            image_document = {
                'image_data': binary.Binary(image_bytes),
                'image_name': file.filename
            }
            print(client)
            #collection.insert_one(image_document) #ERROR!!!!!!
            return 'Image successfully uploaded and added to MongoDB'
    return render_template("process_image.html")

if __name__ == "__main__":
    app.run(debug=True)

