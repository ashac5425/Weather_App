FROM python:3.13

# Set the working directory
WORKDIR /wapp

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

# ✅ EXPOSE the correct port
EXPOSE 8080

# Default command to run the app
CMD ["python", "app.py"]


# FROM python:3.13

# # Set the working directory
# WORKDIR /wapp

# # Install system dependencies needed for PyAudio
# RUN apt-get update && apt-get install -y \
#     build-essential \
#     portaudio19-dev \
#     && apt-get clean \
#     && rm -rf /var/lib/apt/lists/*

# # Copy requirements and install them
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy entire app and credentials
# COPY . .

# # ✅ Set environment variables for Google credentials
# ENV GOOGLE_APPLICATION_CREDENTIALS="/wapp/text-to-speech.json"
# ENV SPEECH_TO_TEXT_CREDENTIALS="/wapp/speech-to-text.json"

# # EXPOSE the correct port
# EXPOSE 8080

# # Default command to run the app
# CMD ["python", "app.py"]

