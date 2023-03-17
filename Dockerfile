FROM python:3.10-alpine

WORKDIR /chatgpturbot

COPY requirements.txt .

RUN apk add --no-cache --virtual .build-deps build-base && \
    pip install -r requirements.txt && \
    apk del .build-deps

COPY chatgpturbot.py .

COPY mdtojson.py .

CMD ["python", "chatgpturbot.py"]