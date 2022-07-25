import os
from dataclasses import dataclass
from pathlib import Path
from typing import List

from environs import Env

@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str


@dataclass
class TgBot:
    token: str
    admin_ids: List[int]
    use_redis: bool


@dataclass
class Miscellaneous:
    other_params: str = None


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig
    db_url: str
    misc: Miscellaneous


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    # return Config(
    #     tg_bot=TgBot(
    #         token=env.str("BOT_TOKEN"),
    #         admin_ids=list(map(int, env.list("ADMINS"))),
    #         use_redis=env.bool("USE_REDIS"),
    #     ),
    #     db=DbConfig(
    #         host=env.str('DB_HOST'),
    #         password=env.str('DB_PASS'),
    #         user=env.str('DB_USER'),
    #         database=env.str('DB_NAME')
    #     ),
    #     db_url=env.str('DATABASE_URL'),
    #     misc=Miscellaneous()
    # )

    return Config(
        tg_bot=TgBot(
            token=os.getenv('BOT_TOKEN'),
            admin_ids=[1348660557],
            use_redis=False,
        ),
        db=DbConfig(
            host="",
            password="",
            user="",
            database="",
        ),
        db_url=os.getenv('DATABASE_URL'),
        misc=Miscellaneous()
    )


db_url = load_config().db_url
# POSTGRES_URI = f"postgresql://{db.user}:{db.password}@{db.host}/{db.database}"
POSTGRES_URI = db_url
# POSTGRES_URI = os.environ["DATABASE_URL"]
# hello
I18N_DOMAIN = "music_bot"
BASE_DIR = Path(__file__).parent
LOCALES_DIR = BASE_DIR / "locales"

# pybabel extract . -o locales/music_bot.pot
# pybabel init -i locales/music_bot.pot -d locales -D music_bot -l uk
# pybabel compile -d locales -D music_bot

# pybabel update -d locales -D music_bot -i locales/music_bot.pot
# pybabel compile -d locales -D music_bot

