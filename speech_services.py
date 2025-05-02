from google.cloud import speech, texttospeech
import os
from dotenv import load_dotenv

load_dotenv()

SPEECH_TO_TEXT_CREDENTIALS = os.getenv("GOOGLE_SPEECH_TO_TEXT_CREDENTIALS")
TEXT_TO_SPEECH_CREDENTIALS = os.getenv("GOOGLE_TEXT_TO_SPEECH_CREDENTIALS")

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

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = SPEECH_TO_TEXT_CREDENTIALS
    client = speech.SpeechClient()
    
    audio = speech.RecognitionAudio(content=audio_file.read())
    config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.OGG_OPUS,
    language_code="en-US",
)

    response = client.recognize(config=config, audio=audio)
    if not response.results:
        print("No transcription found.")
        return ""
    for result in response.results:
        print("Transcript:", result.alternatives[0].transcript)


    transcript = response.results[0].alternatives[0].transcript.strip()
    print(f"Transcript: {transcript}")

    if not transcript:
        print("Empty transcription result.")
        return ""

    return transcript



def convert_text_to_speech(text):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = TEXT_TO_SPEECH_CREDENTIALS
    client = texttospeech.TextToSpeechClient()
    
    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    
    return response.audio_content
