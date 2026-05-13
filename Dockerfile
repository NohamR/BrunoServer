# Use an official Python runtime as a parent image
FROM python:3.11.15-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements file to image
COPY requirements.txt requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY server.py server.py

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run the application
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "server:app"]
