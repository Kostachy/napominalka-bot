FROM python:3.10.9-slim-buster

RUN apt-get update && \
    apt-get install -y gcc libpq-dev && \
    apt clean && \
    rm -rf /var/cache/apt/* \

WORKDIR /napominalka_bot

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x /napominalka_bot/docker/app.sh

CMD ["python", "bot.py"]