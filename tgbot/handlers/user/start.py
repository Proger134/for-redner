import asyncio
import typing
from aiogram import types, Dispatcher

from aiogram.dispatcher.filters import CommandStart, Command
from tgbot.load_all import _

from tgbot.db_api.user_commands import add_user, change_user_language
from tgbot.keyboards.inline import languages_keyboard
from tgbot.middlewares.language import setup_middleware


async def user_help(call: typing.Union[types.Message, types.CallbackQuery], state):
    try:
        message = call.message
    except Exception:
        message = call

    await cancel(message=message, state=state)
    admin_id = call.bot.get("config").tg_bot.admin_ids[0]
    admin = await call.bot.get_chat(admin_id)

    text = "\n".join([
        _("Hi, {user_name}!").format(user_name=call.from_user.first_name),
        _("Just send me name of the song and i will find music for you."),
        "",
        _("▫ /playlists - to see your playlists"),
        _("▫ /artist - to find most popular songs from received artist"),
        _("▫ /album - to find album"),
        _("▫ /set_language - to set language"),
        _("▫ /cancel - to cancel search or to stop queue"),
        "",
        _("📱 Contact me - {admin}").format(admin=admin.get_mention(as_html=True))
    ])
    await message.answer(text)


async def user_start(message: types.Message, state):
    user = await add_user(telegram_id=message.from_user.id, language="en")
    await choose_language(message, state)


async def cancel(message: types.Message, state):
    if state:
        state_name = await state.get_state()
        if state_name is None:
            return

        await state.finish()


async def choose_language(message: types.Message, state):
    await cancel(message, state)
    await message.answer("Choose your language: ", reply_markup=languages_keyboard)


async def set_language(call: types.CallbackQuery, state):
    await call.message.delete()
    language_code = call.data.split(":")[1]
    await change_user_language(call.from_user.id, language_code)

    await user_help_lg(call, state, language_code)


async def user_help_lg(call: typing.Union[types.Message, types.CallbackQuery], state, language):
    try:
        message = call.message
    except Exception:
        message = call

    await cancel(message=message, state=state)
    admin_id = call.bot.get("config").tg_bot.admin_ids[0]
    admin = await call.bot.get_chat(admin_id)

    if language == "uk":
        text = "\n".join([
            "Привіт, {user_name}!".format(user_name=call.from_user.first_name),
            "Просто надішли мені запит для пошуку",
            "",
            "▫ /playlists - твої плейлисти",
            "▫ /artist - пошук виконавця",
            "▫ /album - альбому",
            "▫ /set_language - встановити мову",
            "▫ /cancel - щоб скасувати пошук, або зупинити чергу",
            "",
            "📱 Зв'язатися зі мною - {admin}".format(admin=admin.get_mention(as_html=True))
        ])
    else:
        text = "\n".join([
            "Hi, {user_name}!".format(user_name=call.from_user.first_name),
            "Just send me name of the song and i will find music for you.",
            "",
            "▫ /playlists - to see your playlists",
            "▫ /artist - to find most popular songs from received artist",
            "▫ /album - to find album",
            "▫ /set_language - to set language",
            "▫ /cancel - to cancel search or to stop queue",
            "",
            "📱 Contact me - {admin}".format(admin=admin.get_mention(as_html=True))
        ])

    await message.answer(text)


def register_user_start(dp: Dispatcher):
    dp.register_message_handler(user_start, CommandStart(), state="*")
    dp.register_message_handler(user_help, Command("help"), state="*")
    dp.register_message_handler(choose_language, commands="set_language", state="*")
    dp.register_message_handler(cancel, commands=["cancel", "stop"], state="*")
    dp.register_callback_query_handler(set_language, lambda x: x.data and x.data.startswith("language:"), state="*")
