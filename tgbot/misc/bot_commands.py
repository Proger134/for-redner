from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeChat
from tgbot.load_all import _

base_commands = [
    BotCommand(command="help", description=_("Help from bot")),
    BotCommand(command="playlists", description=_("Get all playlists")),
    BotCommand(command="album", description=_("Find album")),
    BotCommand(command="artist", description=_("Find artist")),
    BotCommand(command="stop", description=_("Clear queue")),
    BotCommand(command="set_language", description=_("Set language"))
]


async def set_bot_commands(bot: Bot):
    await bot.set_my_commands(base_commands)


async def set_admin_bot_commands(bot: Bot, user_id: int):
    await bot.set_my_commands([
        *base_commands,
        BotCommand(command="mailing", description=_("Start mailing")),
        BotCommand(command="count_users", description=_("Get users count"))
    ], scope=BotCommandScopeChat(chat_id=user_id))
