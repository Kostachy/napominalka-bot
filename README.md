# NapominalkaBot

Tech stack:

* Python 3.10
* Aiogram 3.0.0b6
* PostgreSQL + SQLAlchemy + asyncpg driver + alembic
* Redis
* Docker + docker-compose

### How to use

1. git clone `https://github.com/Kostachy/NapominalkaBot.git`
2. Navigate inside project root folder:
`cd NapominalkaBot`
3. Run `pip install -r requirements.txt`
4. Create db
5. Run `alembic upgrade head`
6. Create .env file for developing and .end-prod file for deployment
7. Set .env variables like in the .env.example file
    - `BOT_TOKEN` - token from BotFather
    -  You can leave `USE_WEBHOOK` empty to use long polling and ignore next variables

        - `WEB_SERVER_HOST`
        - `WEB_SERVER_PORT`
        - `WEBHOOK_PATH`
        - `WEBHOOK_SECRET`
        - `BASE_WEBHOOK_URL`

8. Build docker by running `docker compose build`
9. Run container `docker compose up`
