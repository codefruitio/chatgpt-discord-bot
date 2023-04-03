FROM python:3.10-alpine

WORKDIR /luna

COPY requirements.txt .

RUN apk add --no-cache --virtual .build-deps build-base && \
    pip install -r requirements.txt && \
    apk del .build-deps

COPY luna.py .

CMD ["python", "luna.py"]