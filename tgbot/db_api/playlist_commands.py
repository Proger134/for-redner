from sqlalchemy import and_

from tgbot.db_api.models import Playlist


async def get_song(playlist_name: str, song_id: str, telegram_id: int):
    conditions = [
        Playlist.telegram_id == telegram_id,
        Playlist.playlist_name == playlist_name,
        Playlist.song_id == song_id
    ]
    song = await Playlist.query.where(and_(*conditions)).gino.first()
    return song


async def remove_song(playlist_name: str, song_id: str, telegram_id: int):
    conditions = [
        Playlist.telegram_id == telegram_id,
        Playlist.playlist_name == playlist_name,
        Playlist.song_id == song_id
    ]
    status = await Playlist.delete.where(and_(*conditions)).gino.status()
    return status


async def add_song_to_playlist(**kwargs):
    song = await Playlist(**kwargs).create()
    return song


async def show_playlist(playlist_name: str, telegram_id: int):
    conditions = [
        Playlist.telegram_id == telegram_id,
        Playlist.playlist_name == playlist_name
    ]
    songs_playlist = await Playlist.query.where(and_(*conditions)).gino.all()

    return songs_playlist

