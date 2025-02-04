import io
import numpy as np
import sounddevice as sd
from gtts import gTTS
from pydub import AudioSegment


def create_speech(text: str) -> np.ndarray:
    tts = gTTS(text)

    mp3_fp = io.BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)

    audio = AudioSegment.from_file(mp3_fp, format="mp3")

    samples = np.array(audio.get_array_of_samples()).astype(np.float32)
    samples /= np.iinfo(audio.array_type).max

    return samples


def play_speech(speech: np.ndarray, sample_rate: int = 30050):
    sd.play(speech, samplerate=sample_rate)
    sd.wait()