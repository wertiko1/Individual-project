import json
import os

import soundfile as sf
from loguru import logger
from vosk import Model, KaldiRecognizer

from src.settings import ModelSettings


def recognize_audio(mp3_file) -> str | None:
    vosk_model = ModelSettings.VOSK_MODEL
    model = Model(vosk_model)

    recognizer = KaldiRecognizer(model, 16000)
    try:
        with sf.SoundFile(mp3_file) as f:
            while True:
                audio_chunk = f.read(4000)
                if len(audio_chunk) == 0:
                    break
                if recognizer.AcceptWaveform(audio_chunk):
                    result = recognizer.Result()
                    result_json = json.loads(result)
                    if 'text' in result_json:
                        return result_json['text']
        partial_result = recognizer.PartialResult()
        partial_result_json = json.loads(partial_result)
        return partial_result_json.get("partial", "")

    except Exception as e:
        logger.error(f"Error during speech recognition: {e}")
        return None

    finally:
        if os.path.exists(mp3_file):
            os.remove(mp3_file)
            logger.info(f"Deleted temporary WAV file {mp3_file}")
