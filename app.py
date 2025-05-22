
from flask import Flask, request, jsonify, render_template, send_file
import requests
import os
from dotenv import load_dotenv
from weather import get_weather, post_weather
from speech_services import convert_speech_to_text, convert_text_to_speech
from io import BytesIO
from google.cloud import speech
from geotext import GeoText

load_dotenv()

app = Flask(__name__)

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
API_AUDIENCE = os.getenv("AUTH0_API_AUDIENCE")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_SPEECH_TO_TEXT_CREDENTIALS")
# If needed for TTS separately
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_TEXT_TO_SPEECH_CREDENTIALS")

def get_access_token():
    url = f"https://{AUTH0_DOMAIN}/oauth/token"
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "audience": API_AUDIENCE,
        "grant_type": "client_credentials"
    }
    headers = {'content-type': 'application/json'}
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json().get("access_token")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/getweather', methods=['GET'])
def get_weather_route():
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "City parameter is required"}), 400
    token = get_access_token()
    return get_weather(token, city)

@app.route('/postweather', methods=['POST'])
def post_weather_route():
    data = request.get_json()
    if not data or 'city' not in data:
        return jsonify({"error": "City is required"}), 400
    token = get_access_token()
    return post_weather(token, data)




@app.route('/speechtotext', methods=['POST'])
def speech_to_text():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    try:
        audio_file = request.files['audio']
        audio_data = audio_file.read()
        print("Received audio data length:", len(audio_data))

        transcript = convert_speech_to_text(BytesIO(audio_data))

        if not transcript:
            return jsonify({'error': 'Could not transcribe audio'}), 400

        print("Transcript:", transcript)

        # 🔍 Extract cities using GeoText
        places = GeoText(transcript)
        cities = places.cities
        print("Extracted cities:", cities)

        if not cities:
            return jsonify({'error': 'No city found in your sentence'}), 200

        # Return first city found
        return jsonify({'city': cities[0]})

    except Exception as e:
        print("Error in /speechtotext:", e)
        return jsonify({'error': str(e)}), 500
def convert_speech_to_text(audio_file):
    try:
        client = speech.SpeechClient()
        content = audio_file.read()
        print("Audio content size:", len(content))

        audio = speech.RecognitionAudio(content=content)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.WEBM_OPUS,
            sample_rate_hertz=48000,
            language_code="en-US",
        )

        response = client.recognize(config=config, audio=audio)

        if not response.results:
            print("No transcription results.")
            return None

        transcript = response.results[0].alternatives[0].transcript
        print("Transcript:", transcript)
        return transcript

    except Exception as e:
        print("Error in convert_speech_to_text:", e)
        return None
    
    
@app.route('/texttospeech', methods=['POST'])
def text_to_speech():
    data = request.get_json()
    text = data.get('text')
    if not text:
        return jsonify({'error': 'Text is required'}), 400

    audio_content = convert_text_to_speech(text)
    return send_file(
        BytesIO(audio_content),
        mimetype='audio/mp3',
        as_attachment=False,
        download_name='weather.mp3'
    )


if __name__=="__main__":
    app.run(debug=True,host="0.0.0.0",port=8080)



