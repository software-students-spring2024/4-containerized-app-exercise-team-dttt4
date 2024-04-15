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
transcribes them into text and speech.

## Project Layout
This project consists of three parts. Each part operates
in its own docker container.

### Machine Learning Client
The machine learning client uses Pillow to transcribe text 
from image, and IBM Watson speech libraries to 
read the text and output audio. 

### Web App
The web app uses flask and HTML to allow visitors make
 use of the client and look at results. The transcribed images are saved in MongoDB.

### Database
MongoDB is used to store image collections. The collection include name and data. 

## P