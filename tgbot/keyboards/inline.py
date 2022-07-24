from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from tgbot.misc.service import get_song_data

item_callback_data = CallbackData("item", "type", "browse_id")
add_to_playlist_callback_data = CallbackData("pl", "playlist_name", "song_id")

languages_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🇺🇸", callback_data="language:en"),
            InlineKeyboardButton(text="🇺🇦", callback_data="language:uk")
        ]
    ]
)

playlists_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="❤", callback_data="playlist:❤"),
            InlineKeyboardButton(text="🚘", callback_data="playlist:🚘"),
            InlineKeyboardButton(text="🏃‍♂️", callback_data="playlist:🏃‍♂️")
        ]
    ]
)


def show_playlist_keyboard(list_songs):
    markup = InlineKeyboardMarkup()

    for song in list_songs:
        song_id = song.song_id
        song_data = get_song_data(song_id)
        markup.row(InlineKeyboardButton(text=song_data.get("song_name"), callback_data=f"playlist_song:{song_id}"))

    return markup


def song_keyboard(song_id):
    markup = InlineKeyboardMarkup(row_width=3, inline_keyboard=[
        [
            InlineKeyboardButton(text="❤ / 🗑", callback_data=add_to_playlist_callback_data.new("❤", song_id)),
            InlineKeyboardButton(text="🚘 / 🗑", callback_data=add_to_playlist_callback_data.new("🚘", song_id)),
            InlineKeyboardButton(text="🏃‍♂️ / 🗑", callback_data=add_to_playlist_callback_data.new("🏃‍♂️", song_id))
        ]
    ])
    return markup


def menu_list_keyboard(data: dict, step: int, item_type: str):
    markup = InlineKeyboardMarkup()

    items = data[step - 10:step]
    for item in items:
        if item_type == "artist":
            name = item.get("artist")
            artist_id = item.get("browseId")
            markup.row(
                InlineKeyboardButton(text=name, callback_data=item_callback_data.new(item_type, artist_id))
            )
        else:
            title = item.get("name")
            author = item.get("author")
            item_id = item.get("browse_id")
            markup.row(
                InlineKeyboardButton(text=f"{title} - {author}",
                                     callback_data=item_callback_data.new(item_type, item_id))
            )

    if len(data) > 10:
        if step > 10:
            markup.row(InlineKeyboardButton(text="⬅", callback_data=f"step:{step - 10}"))
        else:
            markup.row(InlineKeyboardButton(text="⏺", callback_data="nothing"))

        # markup.insert(InlineKeyboardButton(text="❌", callback_data="cancel"))

        if step < len(data):
            markup.insert(InlineKeyboardButton(text="➡", callback_data=f"step:{step + 10}"))
        else:
            markup.insert(InlineKeyboardButton(text="⏺", callback_data="nothing"))

    return markup
