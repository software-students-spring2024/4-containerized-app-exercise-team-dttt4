import io
import os
from flask import Flask, jsonify, request
from PIL import Image
import pytesseract
from pymongo import MongoClient
from gridfs import GridFS
from bson.objectid import ObjectId
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# MongoDB setup
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client["imagedb"]
fs = GridFS(db)
collection = db["imageCollection"]

@app.route("/process", methods=["POST"])
def process():
    try:
        # Fetch the first unprocessed image document
        image_document = collection.find_one({"is_processed": False})
        if not image_document:
            return jsonify({"error": "No unprocessed images available."}), 404

        # Convert binary data to an image
        image_bytes = io.BytesIO(image_document['image_data'])
        image = Image.open(image_bytes)

        # Extract text from the image using pytesseract
        text = pytesseract.image_to_string(image)
        if text:
            # Update the MongoDB document with the extracted text and mark as processed
            collection.update_one(
                {"_id": image_document['_id']},
                {
                    "$set": {
                        "text": text,
                        "is_processed": True
                    }
                }
            )
            return jsonify({"message": "Image processed and text saved."}), 200
        else:
            return jsonify({"error": "No text could be extracted from the image."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
