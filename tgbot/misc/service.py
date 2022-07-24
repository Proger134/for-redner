from ytmusicapi import YTMusic
from youtube_search import YoutubeSearch
from pytube import YouTube

import os

auth_path = "tgbot/data/auth.json"
yt_music = YTMusic(auth_path)


def get_list_songs(result_data):
    data = []

    for result in result_data:
        song_name = result.get("title")
        video_id = result.get("videoId")
        song_authors = ""
        artists = result.get("artists")
        for artist in artists:
            song_authors += artist.get("name") + " • "

        data.append({
            "name": song_name,
            "author": song_authors.strip(" • "),
            "browse_id": video_id
        })

    return data


def get_list_songs_by_name(text):
    search_results = yt_music.search(text, filter="songs", limit=100)
    return get_list_songs(search_results)


def get_song_data(song_id):
    song_data = yt_music.get_song(videoId=song_id)
    song_title = song_data.get("videoDetails").get("title")
    song_author = song_data.get("videoDetails").get("author")
    song_duration = int(song_data.get("videoDetails").get("lengthSeconds"))

    data = {
        "title": song_title,
        "author": song_author,
        "duration": song_duration,
        "song_name": song_author + " - " + song_title
    }
    return data


def search_video_url(title):
    result = YoutubeSearch(title + "lyrics", max_results=1).to_dict()[0]
    url = "https://www.youtube.com" + result.get("url_suffix")
    return url


def download_song(video_url, title):
    try:
        yt = YouTube(video_url)
        video = yt.streams.filter(only_audio=True).first()

        destination = r'tgbot/data/songs/'
        out_file = video.download(output_path=destination)
        base, ext = os.path.splitext(out_file)
        new_path = "\\".join(base.split("/")[0:-1])
        new_file = new_path + f"\\{title}" + '.mp4'
        os.rename(out_file, new_file)
        return {"new_file": new_file.split("\\")[-1]}
    except Exception as err:
        return False


def get_album(album_id):
    album = yt_music.get_album(album_id)

    artists = album.get("artists")
    song_authors = ""
    for artist in artists:
        song_authors += artist.get("name") + " • "

    return {
        "title": album.get("title"),
        "year": album.get("year"),
        "tracks_count": album.get("trackCount"),
        "artists": song_authors.strip(" • "),
        "tracks":  album.get("tracks")
    }


def get_list_albums_by_name(text):
    search_results = yt_music.search(text, filter="albums", limit=100)
    data = []

    for result in search_results:
        data.append({
            "name": result.get("title"),
            "author": result.get("artists")[0].get("name"),
            "browse_id": result.get("browseId")
        })

    return data


def get_list_artists(artist_name):
    search_results = yt_music.search(artist_name, filter="artists", limit=100)
    return search_results


def get_artist(channel_id):
    artist = yt_music.get_artist(channel_id)

    playlist_id = artist.get("songs").get("browseId")
    try:
        photo = artist.get("thumbnails")[0].get("url")
    except Exception as err:
        photo = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQrCviatijw3cFcADwuxWKdzbkhI63bPOoJxyc39ugnhOv4e7RRk_CTvSy61L4jvhwkKNg&usqp=CAU"
    name = artist.get("name")
    subscribers = artist.get("subscribers")

    playlist = yt_music.get_playlist(playlist_id, limit=20)
    tracks = playlist.get("tracks")[:50]
    tracks = get_list_songs(tracks)

    return {
        "name": name,
        "photo": photo,
        "subscribers": subscribers,
        "songs": tracks
    }


def main():
    # get_list_songs("Wasted")
    # download_song("https://www.youtube.com/watch?v=pqiO8wV4-wc", "hello")
    pass


if __name__ == "__main__":
    main()
