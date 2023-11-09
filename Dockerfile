FROM python:3.10-alpine

WORKDIR /samantha

COPY requirements.txt .

RUN apk add --no-cache --virtual .build-deps build-base && \
    pip install -r requirements.txt && \
    apk del .build-deps

COPY samantha.py .

CMD ["python", "samantha.py"]