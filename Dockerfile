# Use the official Python 3.11 image from the Docker Hub
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install the dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app/

# Expose the port on which the app will run
EXPOSE 8000

# Define the command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "main.wsgi:application"]
