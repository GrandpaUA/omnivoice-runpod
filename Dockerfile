FROM runpod/base:0.6.2-cuda12.2.0

RUN pip install --no-cache-dir torch==2.8.0+cu128 torchaudio==2.8.0+cu128 \
    --extra-index-url https://download.pytorch.org/whl/cu128

RUN pip install --no-cache-dir omnivoice soundfile runpod

COPY handler.py /

CMD ["python", "-u", "/handler.py"]
