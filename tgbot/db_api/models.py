from tgbot.db_api.database import db
from sqlalchemy import sql, Column, Integer, Sequence, BigInteger, String


class User(db.Model):
    __tablename__ = "user"
    sql: sql.Select

    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    telegram_id = Column(BigInteger, primary_key=True)
    language = Column(String(2))


class Playlist(db.Model):
    __tablename__ = 'playlist'
    sql: sql.Select

    id = Column(Integer, Sequence("playlist_id_seq"), primary_key=True)
    telegram_id = Column(BigInteger)
    playlist_name = Column(String(20))
    song_id = Column(String(255))

    def __repr__(self):
        return f"Song {self.song_id}"
