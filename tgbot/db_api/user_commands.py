from tgbot.db_api.models import User


async def get_users_count():
    count = len(await User.query.gino.all())
    return count


async def get_all_users(language: str):
    users = await User.query.where(language == language).gino.all()
    return users


async def get_user(telegram_id: int):
    user = await User.query.where(User.telegram_id == telegram_id).gino.first()
    return user


async def add_user(telegram_id: int, language: str):
    is_user = await get_user(telegram_id=telegram_id)
    if not is_user:
        user = await User(telegram_id=telegram_id, language=language).create()
        return user
    else:
        return is_user


async def change_user_language(telegram_id: int, language: str):
    status = await User.update.values(language=language).where(User.telegram_id == telegram_id).gino.status()
    return status

