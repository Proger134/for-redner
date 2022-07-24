from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from tgbot.load_all import _

from tgbot.handlers.user.common_search import start_menu, list_pagination

from tgbot.misc.service import get_list_songs_by_name


async def start_search(message: types.Message, state: FSMContext):
    """ User enter song name and got list songs """
    text = message.text
    list_songs = get_list_songs_by_name(text=text)

    if len(list_songs) == 0:
        await message.answer(_("Nothing found ☹"))
        return

    await state.set_state("find_song")
    async with state.proxy() as data:
        data["list_items"] = list_songs

    await start_menu(message, list_songs, _("Result (<i>{text}</i>) :").format(text=text), "song")


async def list_songs_pagination(call: types.CallbackQuery, state: FSMContext):
    await list_pagination(call, state, "song")


def register_search(dp: Dispatcher):
    dp.register_message_handler(start_search, state="*")
    dp.register_callback_query_handler(list_songs_pagination, lambda x: x.data and x.data.startswith("step:"), state="find_song")




