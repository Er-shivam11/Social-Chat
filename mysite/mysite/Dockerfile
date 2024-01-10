# Use an official Python runtime as a parent image
FROM python:3.9

# Set environment variables for Python and Django
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=mysite.settings

# Create and set the working directory
WORKDIR /app

# Copy the project code into the container
COPY requirements.txt /app/requirements.txt

# Install project dependencies
RUN pip install -r requirements.txt

# Copy the entire project directory into the container
COPY . /app/


