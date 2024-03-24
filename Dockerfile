# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

RUN pip install pillow

RUN pip install google-cloud-storage

RUN pip install gradio

RUN pip install opencv-python

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx

RUN apt-get update && apt-get install -y \
    libglib2.0-0

RUN pip install torch

RUN pip install torchvision

RUN pip install --upgrade pip

RUN pip install jinja2

# Install Flask
RUN pip install Flask==2.1.0

RUN pip install Werkzeug==0.16.0

RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgtk-3-dev \
    python3-dev \
    python3-numpy \
    python3-pip \
    python3-setuptools

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt



# Run app.py when the container launches
CMD ["python", "app.py"]

