import io
import logging
from os import getenv
from flask import Flask, request, render_template, flash, redirect, url_for, jsonify
from pymongo import MongoClient
from gridfs import GridFS
from bson import binary, ObjectId
from dotenv import load_dotenv
import requests

logging.basicConfig(level=logging.INFO)

load_dotenv()

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

mongo_uri = getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client["imagedb"]
collection = db["imageCollection"]
fs = GridFS(db) 

@app.route("/", methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":
        file = request.files.get("file")
        if file and file.filename:
            try:
                image_byte_array = io.BytesIO()
                file.save(image_byte_array)  # Save the image to byte array
                image_bytes = image_byte_array.getvalue()

                image_document = {
                    "image_data": binary.Binary(image_bytes),
                    "image_name": file.filename,
                    "is_processed": False
                }

                result = collection.insert_one(image_document)
                flash("Image successfully uploaded. Processing will begin shortly.", "success")
            except Exception as e:
                flash(f"Error uploading the image: {e}", "error")
        else:
            flash("No file selected or file is invalid.", "error")
    return render_template("upload_image.html")

@app.route("/list_text")
def list_text():
    # Fetch only processed documents where text is available
    text_documents = collection.find({"is_processed": True}, {"text": 1, "image_name": 1})
    return render_template("list_text.html", text_documents=text_documents)

@app.route('/trigger_process', methods=['POST'])
def trigger_process():
    try:
        # URL of the mlclient.py process route
        mlclient_url = "http://mlclient:5001/process"
        response = requests.post(mlclient_url)
        if response.status_code == 200:
            flash("Processing triggered successfully.", "success")
        else:
            flash(f"Failed to trigger processing: {response.text}", "error")
    except requests.exceptions.RequestException as e:
        flash(f"Error triggering processing: {e}", "error")
    return redirect(url_for('upload_image'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8080)
