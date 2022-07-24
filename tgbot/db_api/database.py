from gino import Gino

from tgbot.config import POSTGRES_URI

db = Gino()


async def create_database():
    await db.set_bind(POSTGRES_URI)
    # await db.gino.drop_all()
    await db.gino.create_all()

