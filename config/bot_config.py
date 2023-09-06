from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str


@dataclass
class PostgresConfig:
    db_host: str
    db_port: int
    db_user: str
    db_pass: str
    db_name: str


@dataclass
class Config:
    tg_bot: TgBot
    postgres: PostgresConfig


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(tg_bot=TgBot(token=env('BOT_TOKEN')),
                  postgres=PostgresConfig(db_name=env('DB_NAME'),
                                          db_host=env("DB_HOST"),
                                          db_port=env("DB_PORT"),
                                          db_user=env("DB_USER"),
                                          db_pass=env("DB_PASS")))


config: Config = load_config()
