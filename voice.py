import speech_recognition as sr
import sounddevice as sd
import numpy as np

recognizer = sr.Recognizer()

def listen() -> str:
    with sr.Microphone() as source:
        print("Say something...")
        # recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=50, phrase_time_limit=10)

        heard: str = ""

    try:
        text = recognizer.recognize_google(audio)
        heard += text
        print("You said:", text)

        # play_audio_from_buffer(audio)
    
    except sr.UnknownValueError:
        print("Could not understand the audio")
    except sr.RequestError:
        print("Could not request results from Google Speech Recognition service")
    except sr.WaitTimeoutError:
        print("Timeout")
    finally:
        return heard

def play_audio_from_buffer(audio):
    audio_data = np.frombuffer(audio.get_raw_data(), dtype=np.int16)

    amplification_factor = 2
    audio_data = np.clip(audio_data * amplification_factor, -32768, 32767)

    sd.play(audio_data, samplerate=audio.sample_rate)
    sd.wait()


while True:
    command = listen().lower()
    if "exit" in command:
        break
