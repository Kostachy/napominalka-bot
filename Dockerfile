FROM python:3.10.9-slim-buster

WORKDIR /napominalka_bot

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod a+x /napominalka_bot/docker/app.sh

CMD ["python", "bot.py"]