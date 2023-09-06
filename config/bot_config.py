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
class RedisConfig:
    redis_host: str
    redis_pass: str
    redis_port: int


@dataclass
class Config:
    tg_bot: TgBot
    postgres: PostgresConfig
    redis_db: RedisConfig


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(tg_bot=TgBot(token=env('BOT_TOKEN')),
                  postgres=PostgresConfig(db_name=env('DB_NAME'),
                                          db_host=env("DB_HOST"),
                                          db_port=env("DB_PORT"),
                                          db_user=env("DB_USER"),
                                          db_pass=env("DB_PASS")),
                  redis_db=RedisConfig(redis_host=env('REDIS_HOST'),
                                       redis_pass=env('REDIS_PASS'),
                                       redis_port=env('REDIS_PORT')))


config: Config = load_config()
