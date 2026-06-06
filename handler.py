import runpod
import torch
import soundfile as sf
import base64
import io
from omnivoice import OmniVoice

model = None

def load_model():
    global model
    if model is None:
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
    )

    buf = io.BytesIO()
    sf.write(buf, audio[0], 24000, format="WAV")
    buf.seek(0)
    audio_b64 = base64.b64encode(buf.read()).decode("utf-8")

    return {"audio_base64": audio_b64, "sample_rate": 24000}

runpod.serverless.start({"handler": handler})
