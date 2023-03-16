FROM python:3.10-alpine

WORKDIR /chatgpturbot

COPY requirements.txt .

COPY notes /notes

RUN apk add --no-cache --virtual .build-deps build-base && \
    pip install -r requirements.txt && \
    apk del .build-deps

COPY chatgpturbot.py .

CMD ["python", "chatgpturbot.py"]