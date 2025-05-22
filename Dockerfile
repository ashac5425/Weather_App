FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install system dependencies needed for PyAudio
RUN apt-get update && apt-get install -y \
    build-essential \
    portaudio19-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Default command
CMD ["python", "app.py"]

 

# # Use official Python image
# FROM python:3.10-slim

# # Set working directory inside container
# WORKDIR /app

# # Copy requirements first and install dependencies
# COPY requirements.txt .

# # Install dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy the rest of the app code
# COPY . .

# # Expose the Flask app's port
# EXPOSE 8080

# # Set environment variables for Flask
# ENV FLASK_APP=app.py
# ENV FLASK_RUN_HOST=0.0.0.0
# ENV FLASK_RUN_PORT=8080

# # Run the app
# CMD ["flask", "run"]
