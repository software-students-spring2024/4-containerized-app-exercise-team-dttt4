"""
This module contains a Flask web application that processes images.
"""

import io
import logging
from os import getenv
import requests
from flask import Flask, request, render_template, flash, redirect, url_for, send_file
from pymongo import MongoClient
from PIL import Image
from bson import binary
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)

load_dotenv()

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

mongo_uri = getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client["imagedb"]
collection = db["imageCollection"]


@app.route("/", methods=["GET", "POST"])
def process_image():
    """
    Handles the image upload via POST request and saves it to MongoDB.
    Flashes messages based on the success or failure of the operation.
    """

    if request.method == "POST":
        logging.info("Received POST request with files: %s", request.files)
        if "file" not in request.files:
            flash("No file part", "error")
            return redirect(url_for("process_image"))

        file = request.files["file"]
        if file.filename == "":
            flash("No selected file", "error")
            return redirect(url_for("process_image"))

        if file:
            try:
                image = Image.open(file.stream)
                image_byte_array = io.BytesIO()
                image.save(image_byte_array, format=image.format)
                image_bytes = image_byte_array.getvalue()

                image_document = {
                    "image_data": binary.Binary(image_bytes),
                    "image_name": file.filename,
                    "is_processed": False,
                }

                collection.insert_one(image_document)
                flash("Image successfully uploaded and added to MongoDB", "success")
                response = requests.post("http://mlclient:5001/process", files={'file': ('image.jpg', io.BytesIO(image_bytes), 'image/jpeg')})
                if response.status_code == 200:
                    flash("Audio file processed successfully", "success")
                    audio_file_stream = io.BytesIO(response.content)
                    audio_file_stream.seek(0)  # Ensure the cursor is at the start of the stream
                    return send_file(
                        audio_file_stream,
                        mimetype="audio/wav",
                        as_attachment=True,
                        attachment_filename="output.wav"
                    )
                else:
                    flash("Failed to process image for audio", "error")
            except (
                IOError
            ) as e:  
                logging.error("An error occurred while processing the image: %s", e)
                flash(f"Error processing the image: {e}", "error")

    return render_template("process_image.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8080)
