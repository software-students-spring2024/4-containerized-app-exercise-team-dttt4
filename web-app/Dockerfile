# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install any needed packages specified in requirements.txt
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Make port 5000 available to the world outside this container
EXPOSE 8080

# Define environment variable
ENV NAME WebApp

# Run app.py when the container launches
CMD ["python", "app.py", "--host=0.0.0.0", "--port=8080"]

