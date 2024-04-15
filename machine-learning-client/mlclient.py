"""ML Module for processing images and extracting text."""

import io
import os
from flask import Flask, jsonify
from PIL import Image
import pytesseract
from pymongo import MongoClient
from dotenv import load_dotenv
import logging

load_dotenv()

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client["imagedb"]
collection = db["imageCollection"]


@app.route("/process", methods=["POST"])
def process():
    """Process the first image extract text, and update the document as processed."""
    #try:
    image_document = collection.find_one({"is_processed": False})
    if not image_document:
        return jsonify({"error": "No unprocessed images available."}), 404

    logging.info("Image found, attempting to process.")
    image_bytes = io.BytesIO(image_document["image_data"])
    logging.info("getting image bytes")
    image = Image.open(image_bytes)
    logging.info("opening image")
    text = pytesseract.image_to_string(image)
    if text:
        logging.info("Text extracted, updating the database.")
        collection.update_one(
            {"_id": image_document['_id']},
            {
                "$set": {
                    "text": text,
                    "is_processed": True
                }
            }
        )
        logging.info("Database updated")
        return jsonify({"message": "Image processed and text saved."}), 200

    return jsonify({"error": "No text could be extracted from the image."}), 400
    #except IOError as e:
        #return jsonify({"error": str(e)}, 500)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
