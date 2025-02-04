import google.generativeai as genai
import re
import os
from threading import Thread
import tts
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

chat = model.start_chat()


def prompt(prompt: str):
    if not prompt.strip():
        print("empty prompt")
        return

    try:
        response = chat.send_message(prompt)
    
        text = response.text
        print(text)

        text = re.sub(r"\*\*.*?\*\*", "", text)
        text = re.sub(r"\*.*?\*", "", text)
        text = re.sub(r"~.*?~", "", text)
        text = re.sub(r"`.*?`", "", text)
        text = re.sub(r'\b(e\.g\.|i\.e\.)\b', 'for example', text)

        sentences = text.split('.')

        current_speech = tts.create_speech(sentences[0])

        speech_thread: Thread = Thread(target=tts.play_speech, args=[current_speech]);
        speech_thread.start()

        sentences = [s.replace('*', '').strip() for s in sentences if s.strip()]

        print(sentences)

        for i in range(1, len(sentences)):
            if speech_thread.is_alive():
                if i != len(sentences):
                    current_speech = tts.create_speech(sentences[i])

                speech_thread.join()
                
                speech_thread = Thread(target=tts.play_speech, args=[current_speech])
                speech_thread.start()

    except Exception:
        print('Some error occured')



while True:
    user_input = input("Prompt: ")
    if user_input == 'q':
        break

    prompt(user_input)
