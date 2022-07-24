import os

from aiogram import types, Dispatcher
from tgbot.load_all import _

from tgbot.db_api.playlist_commands import show_playlist, get_song, remove_song, add_song_to_playlist
from tgbot.keyboards.inline import playlists_keyboard, add_to_playlist_callback_data, show_playlist_keyboard, song_keyboard
from tgbot.misc.service import get_song_data


async def show_playlists(message: types.Message):
    await message.answer(_("Your playlists:"), reply_markup=playlists_keyboard)


async def show_songs_playlist(call: types.CallbackQuery):
    """ Show user playlist """
    playlist_name = call.data.split(":")[1]
    songs = await show_playlist(playlist_name, call.from_user.id)

    if not songs:
        await call.message.answer(_("Playlist <b>{playlist_name}</b> is empty").format(playlist_name=playlist_name))
        return

    markup = show_playlist_keyboard(songs)
    await call.message.answer(_("Playlist {playlist_name} songs:").format(playlist_name=playlist_name), reply_markup=markup)


async def add_song(call: types.CallbackQuery, callback_data: dict):
    """ Add song to playlist """
    playlist_name = callback_data.get("playlist_name")
    song_id = callback_data.get("song_id")

    song_data = get_song_data(song_id)

    is_in_playlist = await get_song(playlist_name, song_id, call.from_user.id)
    if not is_in_playlist:
        song = await add_song_to_playlist(telegram_id=call.from_user.id, playlist_name=playlist_name,
                                          song_id=song_id)
        await call.answer(_("Song {name} added to playlist {playlist_name}").format(
            name=song_data.get('song_name'),
            playlist_name=playlist_name)
        )
    else:
        await remove_song(playlist_name, song_id, call.from_user.id)
        await call.answer(_("Song {name} removed from playlist {playlist_name}").format(
            name=song_data.get('song_name'),
            playlist_name=playlist_name
        ))


def register_playlists(dp: Dispatcher):
    dp.register_message_handler(show_playlists, commands=["playlists", "playlist"], state="*")
    dp.register_callback_query_handler(show_songs_playlist, lambda x: x.data and x.data.startswith("playlist:"), state="*")
    dp.register_callback_query_handler(add_song, add_to_playlist_callback_data.filter(), state="*")
