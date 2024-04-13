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

    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        print(f"An error occurred while processing the image: {e}")
        return None

def text_to_audio(text, output_path):
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
    except Exception as e:
        print(f"Failed to convert text to speech: {e}")

def main():
    image_path = 'images/test.jpg'  
    output_audio_path = 'output_audio.wav'  

    
    text = text_from_image(image_path)
    if text:
        print("Extracted Text:", text)
        text_to_audio(text, output_audio_path)
    else:
        print("No text could be extracted from the image.")

if __name__ == "__main__":
    main()
