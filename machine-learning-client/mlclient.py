"""This module provides functions to convert text from images to audio using IBM Watson."""

import os
from dotenv import load_dotenv
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from PIL import Image
import pytesseract

load_dotenv()

API_KEY = os.getenv('IBM_API_KEY')
SERVICE_URL = os.getenv('IBM_SERVICE_URL')
authenticator = IAMAuthenticator(API_KEY)
text_to_speech = TextToSpeechV1(authenticator=authenticator)
text_to_speech.set_service_url(SERVICE_URL)

def text_from_image(image_path):
    """Extract text from the specified image file.

    Args:
        image_path (str): The path to the image file from which to extract text.

    Returns:
        str or None: The extracted text, or None if the extraction fails.
    """
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return text
    except IOError as e:
        print(f"An error occurred while opening the image: {e}")
        return None

def text_to_audio(text, output_path):
    """Extract audio from text.

    Args:
        text: String to be converted to audio
        output_path (str): The path to the area on local machine where audio file should go

    Returns:
        None: Prints string if file is uploaded succesfully. 
    """
    try:
        with open(output_path, 'wb') as audio_file:
            audio_file.write(
                text_to_speech.synthesize(
                    text,
                    voice='en-US_AllisonV3Voice',
                    accept='audio/wav'
                ).get_result().content
            )
        print(f"Audio file created at {output_path}")
    except IOError as e:
        print(f"Failed to convert text to speech: {e}")

def main():
    """Process an image to extract text and convert it to audio."""
    image_path='images/test.jpg'
    output_audio_path='output_audio.wav'

    text = text_from_image(image_path)
    if text:
        print("Extracted Text:", text)
        text_to_audio(text, output_audio_path)
    else:
        print("No text could be extracted from the image.")

if __name__ == "__main__":
    main()
