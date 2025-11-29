from gtts import gTTS
from pydub import AudioSegment as AS
import tempfile
import os
import speech_recognition as sr

def text_to_speech(text, accent = 'en'):
    tts = gTTS(text = text, lang = accent)
    tts.save(f"output.mp3")
    return f"output.mp3"

def transcribe(uploaded_file):
    with tempfile.NamedTemporaryFile(delete = False, suffix = ".wav") as temp_file:
        file_path = temp_file.name
        temp_file.write(uploaded_file.read())
    
    audio = AS.from_file(file_path)
    audio = audio.set_frame_rate(16000).set_channels(1)
    audio.export(file_path, format = "wav")
    # Speech recognizer
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source :
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
            return text
        except sr.UnknownValueError:
            return "could not understand the audio please try again."
        except sr.RequestError:
            return " API error. Check internet connection."

    os.remove(file_path)
    return "Error"
