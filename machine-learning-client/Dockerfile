# Use an official Python 3.10 runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies required by the application
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Install pipenv
RUN pip install pipenv

# Copy the Pipfile and Pipfile.lock into the container at /app
COPY Pipfile Pipfile.lock /app/

# Install Python dependencies
RUN pipenv install --deploy

# Copy the rest of the application
COPY . /app

# Expose port 80 for the application
EXPOSE 5001

# Set environment variable
ENV NAME World

# Command to run the application
CMD ["pipenv", "run", "python", "mlclient.py"]
