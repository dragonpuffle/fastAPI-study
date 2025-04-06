from dataclasses import dataclass

from environs import Env


@dataclass
class DatabaseConfig:
    database: str


@dataclass
class Config:
    db: DatabaseConfig
    secret_key: str
    debug: bool


def load_config(path: str = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        DatabaseConfig(database=env("DATABASE_URL")),
        secret_key=env("SECRET_KEY"),
        debug=env.bool("DEBUG", default=False),
    )
