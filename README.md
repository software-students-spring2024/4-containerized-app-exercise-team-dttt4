![Lint-free](https://github.com/nyu-software-engineering/containerized-app-exercise/actions/workflows/lint.yml/badge.svg)
![ML Client](https://github.com/software-students-spring2024/4-containerized-app-exercise-team-dttt4/actions/workflows/mlclient.yml/badge.svg)
![Web App](https://github.com/software-students-spring2024/4-containerized-app-exercise-team-dttt4/actions/workflows/webapp.yml/badge.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# Containerized App Exercise

Build a containerized app that uses machine learning. See [instructions](./instructions.md) for details.


## Team members

Deniz Qian: https://github.com/dq2024 \
Somyung Kim: https://github.com/troy-skim \
Terrance Chen: https://github.com/tchen0125 \
Kim Young: https://github.com/Kyoung655

## Project Description
This project is a photo transcription web app 
which reads from user provided photos and 
transcribes them into text.

## Project Layout
This project consists of three parts. Each part operates
in its own docker container.

### Machine Learning Client
The machine learning client uses Pillow and pytesseract to transcribe text 
from image. 

### Web App
The web app uses flask and HTML to allow visitors make
 use of the client and look at results. The transcribed images are saved in MongoDB.

### Database
MongoDB is used to store image collections. The collection include name and data. 

## Project Instructions

### System Requirements
- Python 3.9 or higher

### Install Dependencies
Ensure Flask, pytesseract, Pillow, python-dotenv, pymongo are installed. They should be automatically installed. \
If not:
```
pip install Flask pytesseract Pillow python-dotenv pymongo
```

### Run the Application
```
docker-compose up --build
```
0. It should be running at http://127.0.0.1:8080/ 
1. Click 'choose file' and select your image (JPG, JPEG)
2. Click 'Upload'
3. Click 'Trigger Processing' to transcribe
4. Click 'View Text Transcriptions' to look at current and previous results


### Shutdown the Application
docker-compose down    
