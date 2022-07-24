from typing import Tuple, Any

from aiogram import types
from aiogram.contrib.middlewares.i18n import I18nMiddleware

from tgbot.config import I18N_DOMAIN, LOCALES_DIR
from tgbot.db_api.user_commands import get_user


async def get_lang(user_id):
    user = await get_user(telegram_id=user_id)
    if user:
        lang = user.language
        return lang


class ACLMiddleware(I18nMiddleware):
    async def get_user_locale(self, action: str, args: Tuple[Any]):
        user = types.User.get_current()
        return await get_lang(user.id) or user.locale


def setup_middleware(dp):
    i18n = ACLMiddleware(I18N_DOMAIN, LOCALES_DIR)
    dp.middleware.setup(i18n)
    return i18n


