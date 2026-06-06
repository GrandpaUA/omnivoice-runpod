FROM nvidia/cuda:12.2.0-runtime-ubuntu22.04

RUN apt-get update && apt-get install -y python3 python3-pip && \
    ln -s /usr/bin/python3 /usr/bin/python

RUN pip3 install --no-cache-dir torch==2.8.0+cu128 torchaudio==2.8.0+cu128 \
    --extra-index-url https://download.pytorch.org/whl/cu128

RUN pip3 install --no-cache-dir omnivoice soundfile runpod

COPY handler.py /

CMD ["python3", "-u", "/handler.py"]
