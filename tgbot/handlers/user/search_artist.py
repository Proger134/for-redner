from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from tgbot.load_all import _

from tgbot.handlers.user.common_search import start_menu, list_pagination
from tgbot.handlers.user.start import cancel
from tgbot.keyboards.inline import menu_list_keyboard, item_callback_data
from tgbot.misc.service import get_list_artists, get_artist


async def search_artist_start(message: types.Message, state: FSMContext):
    await cancel(message, state)
    await message.answer(_("Enter artist name"))
    await state.set_state("find_artist")


async def search_artist(message: types.Message, state: FSMContext):
    artist_name = message.text
    list_artists = get_list_artists(artist_name)

    if len(list_artists) == 0:
        await state.finish()
        await message.answer(_("Nothing found ☹"))
        return

    await state.update_data(list_items=list_artists)
    await start_menu(message, list_artists,
                     text=_("Artists by name <b>{artist_name}</b>:").format(artist_name=artist_name), item_type="artist")


async def artist_pagination(call: types.CallbackQuery, state: FSMContext):
    await list_pagination(call, state, "artist")


async def artist_songs(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    artist_playlist_id = callback_data.get("browse_id")
    artist = get_artist(artist_playlist_id)
    list_songs = artist.get("songs")

    if len(list_songs) == 0:
        await call.message.answer(_("Nothing found ☹"))
        await state.finish()
        return

    text = "\n".join([
        _("Nickname: <b>{artist_name}</b>").format(artist_name=artist.get('name')),
        _("Subscribers on youtube: <b>{artist_subscribers}</b>").format(artist_subscribers=artist.get('subscribers'))
    ])

    await state.set_state("find_song")
    await state.update_data(list_items=list_songs)

    markup = menu_list_keyboard(list_songs, 10, "song")
    await call.message.answer_photo(photo=artist.get("photo"), caption=text,
                                    reply_markup=markup)


def register_artist_search(dp: Dispatcher):
    dp.register_message_handler(search_artist_start, commands=["artist"], state="*")
    dp.register_message_handler(search_artist, state="find_artist")
    dp.register_callback_query_handler(artist_pagination, lambda x: x.data and x.data.startswith("step:"), state="find_artist")
    dp.register_callback_query_handler(artist_songs, item_callback_data.filter(type="artist"), state="find_artist")




