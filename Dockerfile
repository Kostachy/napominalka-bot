FROM python:3.10

WORKDIR /napominalka_bot

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x /napominalka_bot/docker/app.sh

CMD ["python", "bot.py"]