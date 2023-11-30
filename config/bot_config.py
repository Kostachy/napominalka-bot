from typing import Literal

from dataclasses import dataclass

from environs import Env


@dataclass
class TgBot:
    token: str
    mode: Literal['DEV', 'TEST', 'PROD']


@dataclass
class PostgresConfig:
    db_host: str
    db_port: int
    db_user: str
    db_pass: str
    db_name: str
    db_name_test: str


@dataclass
class RedisConfig:
    redis_host: str
    redis_pass: str
    redis_port: int


@dataclass
class WebhookConfig:
    USE_WEBHOOK: bool
    WEB_SERVER_HOST: str
    WEB_SERVER_PORT: int
    WEBHOOK_PATH: str
    WEBHOOK_SECRET: str
    BASE_WEBHOOK_URL: str


@dataclass
class Config:
    tg_bot: TgBot
    postgres: PostgresConfig
    redis_db: RedisConfig
    webhook_config: WebhookConfig


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        tg_bot=TgBot(token=env("BOT_TOKEN"),
                     mode=env("MODE")),
        postgres=PostgresConfig(
            db_name=env("DB_NAME"),
            db_name_test=env("DB_NAME_TEST"),
            db_host=env("DB_HOST"),
            db_port=env("DB_PORT"),
            db_user=env("DB_USER"),
            db_pass=env("DB_PASS"),
        ),
        redis_db=RedisConfig(
            redis_host=env("REDIS_HOST"),
            redis_pass=env("REDIS_PASS"),
            redis_port=env("REDIS_PORT"),
        ),
        webhook_config=WebhookConfig(
            USE_WEBHOOK=env("USE_WEBHOOK"),
            WEB_SERVER_HOST=env("WEB_SERVER_PORT"),
            WEB_SERVER_PORT=env("WEB_SERVER_PORT"),
            WEBHOOK_PATH=env("WEBHOOK_PATH"),
            WEBHOOK_SECRET=env("WEBHOOK_SECRET"),
            BASE_WEBHOOK_URL=env("BASE_WEBHOOK_URL"),
        ),
    )


config: Config = load_config()
