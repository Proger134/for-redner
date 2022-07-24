import os

from aiogram import types, Dispatcher
from aiogram.types import InputFile
from tgbot.load_all import _

from tgbot.keyboards.inline import song_keyboard, item_callback_data
from tgbot.misc.service import get_song_data, search_video_url, download_song


async def get_song(call: types.CallbackQuery, callback_data: dict):
    """ Send song to user """
    song_id = callback_data.get("browse_id")

    song_data = get_song_data(song_id)
    song_author = song_data.get("author")
    song_title = song_data.get("title")
    song_duration = song_data.get("duration")
    title = f"{song_author} - {song_title}"

    # check is the song in folder with downloaded songs
    in_folder = False
    for (dirpath, dirnames, filenames) in os.walk("tgbot/data/songs"):
        if title + ".mp4" in filenames:
            in_folder = True
            break

    markup = song_keyboard(song_id)

    # send audio with song or issue
    if in_folder:
        song = InputFile(path_or_bytesio=f"tgbot/data/songs/{title}.mp4")
        await call.message.answer_audio(audio=song, title=title.split(" - ")[1], reply_markup=markup,
                                        performer=song_author, duration=song_duration)
    else:
        song_link = search_video_url(title)
        dw_song = download_song(song_link, title)
        if not dw_song:
            await call.answer(_("I can't download this song {song_title}").format(song_title=song_title))
        else:
            song = InputFile(path_or_bytesio=f"tgbot/data/songs/{dw_song['new_file']}")
            await call.message.answer_audio(audio=song, title=title.split(" - ")[1], reply_markup=markup,
                                            performer=song_author, duration=song_duration)


async def send_playlist_song(call: types.CallbackQuery):
    """ Send song from playlist by title """
    song_id = call.data.split(":")[1]
    await call.answer("")

    song_data = get_song_data(song_id)
    song_name = song_data.get("song_name")

    in_folder = False
    for (dirpath, dirnames, filenames) in os.walk("tgbot/data/songs"):
        if song_name + ".mp4" in filenames:
            in_folder = True
            break

    markup = song_keyboard(song_id)

    # send audio with song or issue
    if not in_folder:
        song_link = search_video_url(song_name)
        dw_song = download_song(song_link, song_name)
        if not dw_song:
            await call.answer(_("I can't download this song {song_name}").format(song_name=song_name))
            return

    song = InputFile(path_or_bytesio=f"tgbot/data/songs/{song_name}.mp4")
    await call.message.answer_audio(audio=song, title=song_data.get("title"), reply_markup=markup,
                                    performer=song_data.get("author"), duration=song_data.get("duration"))


def register_send_song(dp: Dispatcher):
    dp.register_callback_query_handler(get_song, item_callback_data.filter(type="song"), state="*")
    dp.register_callback_query_handler(send_playlist_song, lambda x: x.data and x.data.startswith("playlist_song:"), state="*")



