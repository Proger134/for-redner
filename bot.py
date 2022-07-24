import asyncio
import logging

from tgbot.load_all import dp, bot
from tgbot.db_api.database import create_database
from tgbot.filters.admin import AdminFilter
from tgbot.handlers.admin import register_admin
from tgbot.handlers.user.common_search import register_common_search
from tgbot.handlers.user.playlists import register_playlists
from tgbot.handlers.user.search import register_search
from tgbot.handlers.user.search_album import register_search_album
from tgbot.handlers.user.search_artist import register_artist_search
from tgbot.handlers.user.send_song import register_send_song
from tgbot.handlers.user.start import register_user_start
from tgbot.middlewares.db import DbMiddleware
from tgbot.middlewares.throttling import ThrottlingMiddleware
from tgbot.misc.bot_commands import set_bot_commands

logger = logging.getLogger(__name__)


def register_all_middlewares(dp):
    dp.setup_middleware(DbMiddleware())
    # dp.setup_middleware(ThrottlingMiddleware(5))


def register_all_filters(dp):
    dp.filters_factory.bind(AdminFilter)


def register_all_handlers(dp):
    register_admin(dp)
    register_user_start(dp)
    register_playlists(dp)
    register_common_search(dp)
    register_send_song(dp)
    register_artist_search(dp)
    register_search_album(dp)
    register_search(dp)


async def main():
    logger.info("Starting bot")

    # connect db
    await create_database()

    register_all_middlewares(dp)
    register_all_filters(dp)
    register_all_handlers(dp)

    await set_bot_commands(bot)

    # start
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
