FROM python:3.11-bookworm

RUN apt-get update \
    && apt-get install -y libgl1-mesa-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app
RUN pip install -r requirements.lock

CMD [ "python", "/app/detect_track.py" ]
