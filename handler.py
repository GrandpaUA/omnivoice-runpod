import runpod
import torch
import soundfile as sf
import base64
import io
import os
import urllib.request
from omnivoice import OmniVoice

model = None
SPEAKER_PATH = "/speaker.wav"
SPEAKER_URL = "https://raw.githubusercontent.com/GrandpaUA/omnivoice-runpod/main/speaker.wav"

def load_model():
    global model
    if model is None:
        if not os.path.exists(SPEAKER_PATH):
            urllib.request.urlretrieve(SPEAKER_URL, SPEAKER_PATH)
        model = OmniVoice.from_pretrained(
            "k2-fsa/OmniVoice",
            device_map="cuda:0",
            dtype=torch.float16
        )
    return model

def handler(job):
    job_input = job["input"]
    text = job_input.get("text", "")
    speed = job_input.get("speed", 0.85)

    if not text:
        return {"error": "No text provided"}

    m = load_model()
    audio = m.generate(
        text=text,
        speed=speed,
        language="Ukrainian",
        ref_audio=SPEAKER_PATH,
    )

    buf = io.BytesIO()
    sf.write(buf, audio[0], 24000, format="WAV")
    buf.seek(0)
    audio_b64 = base64.b64encode(buf.read()).decode("utf-8")

    return {"audio_base64": audio_b64, "sample_rate": 24000}

runpod.serverless.start({"handler": handler})
