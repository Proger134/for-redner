from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from tgbot.load_all import _

from tgbot.handlers.user.common_search import start_menu, list_pagination
from tgbot.handlers.user.start import cancel
from tgbot.keyboards.inline import item_callback_data
from tgbot.misc.service import get_list_albums_by_name, get_album, get_list_songs


async def start_search_album(message: types.Message, state: FSMContext):
    """ Start searching album """
    await cancel(message, state)
    await message.answer(_("Enter album name"))
    await state.set_state("find_album")


async def search_album(message: types.Message, state: FSMContext):
    """ Return list albums """
    title = message.text
    list_items = get_list_albums_by_name(title)

    if len(list_items) == 0:
        await message.answer(_("Nothing found ☹"))
        await state.finish()
        return

    await state.update_data(list_items=list_items)

    await start_menu(message, list_items, text=_("Albums {title}:").format(title=title), item_type="album")


async def album_pagination(call: types.CallbackQuery, state: FSMContext):
    """ Pagination for list albums """
    await list_pagination(call, state, "album")


async def album_songs(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    """ Return list song from album """
    album_id = callback_data.get("browse_id")
    album = get_album(album_id)
    songs = album.get("tracks")
    list_songs = get_list_songs(songs)

    if len(list_songs) == 0:
        await call.message.answer(_("Nothing found ☹"))
        await state.finish()
        return

    text = "\n".join([
        f"{album.get('title')} - {album.get('artists')}",
        _("Tracks count: {tracks_count}").format(tracks_count=album.get('tracks_count')),
        _("Year: {year}").format(year=album.get('year'))
    ])

    await state.set_state("find_song")
    await state.update_data(list_items=list_songs)
    await start_menu(call.message, list_songs, text=text, item_type="song")


def register_search_album(dp: Dispatcher):
    dp.register_message_handler(start_search_album, commands=["album"], state="*")
    dp.register_message_handler(search_album, state="find_album")
    dp.register_callback_query_handler(album_pagination, lambda x: x.data and x.data.startswith("step:"), state="find_album")
    dp.register_callback_query_handler(album_songs, item_callback_data.filter(type="album"), state="find_album")

