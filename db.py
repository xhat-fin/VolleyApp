from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, relationship
from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from datetime import datetime


database = "sqlite:///VolleyApp.db"
engine = create_engine(database)
Session = sessionmaker(autoflush=False)


class Base(DeclarativeBase):
    pass


class Game(Base):
    __tablename__ = 'game'

    game_id = Column(Integer, primary_key=True, index=True)
    title_game = Column(String)
    description = Column(String)
    need_players = Column(Integer)
    date_create = Column(DateTime, default=datetime.now)
    date_update = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    games = relationship("GameNotes", back_populates="game")


class Players(Base):
    __tablename__ = 'player'

    player_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    games = relationship("GameNotes", back_populates='players')



class GameNotes(Base):
    __tablename__ = 'game_notes'

    game_notes_id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("game.game_id"))
    player_id = Column(Integer, ForeignKey("player.player_id"))

    game = relationship("Game", back_populates='games')
    players = relationship("Players", back_populates='games')


def init_db(Base_class):
    Base_class.metadata.create_all(bind=engine)


def select():
    try:
        with Session(autoflush=False, bind=engine) as db:
            games = db.query(Game).order_by(Game.game_id.desc()).all()

        response = []
        for game in games:
            response.append(
                {
                    'game_id': game.game_id,
                    'title_game': game.title_game,
                    'description': game.description,
                    'need_players': game.need_players,
                    'created_date': game.date_create,
                    'updated_date': game.date_update
                }
            )

        return response
    except Exception as e:
        print(e)


def select_game(game_id):
    try:
        with Session(autoflush=False, bind=engine) as db:
            game = db.query(Game).filter(Game.game_id == game_id).first()
        response = {
                    'game_id': game.game_id,
                    'title_game': game.title_game,
                    'description': game.description,
                    'need_players': game.need_players,
                    'created_date': game.date_create,
                    'updated_date': game.date_update
                }
        return response
    except Exception as e:
        print(e)


def insert_game(title_game, description, need_players):
    try:
        with Session(autoflush=False, bind=engine) as db:
            game = Game(title_game=title_game, description=description, need_players=need_players)
            db.add(game)
            db.commit()
            new_game = {
                    'title_game': game.title_game,
                    'description': game.description,
                    'need_players': game.need_players
                }
        return new_game
    except Exception as e:
        print(e)


def update_game(game_id, new_title_game, new_description, new_need_players):
    try:
        with Session(autoflush=False, bind=engine) as db:
            game = db.query(Game).filter(Game.game_id == game_id).first()
            game.title_game = new_title_game
            game.description = new_description
            game.need_players = new_need_players
            db.commit()
            new_game = {
                    'title_game': game.title_game,
                    'description': game.description,
                    'need_players': game.need_players
                }
            return new_game
    except Exception as e:
        print(e)


def create_players(username, password_hash):
    try:
        with Session(autoflush=False, bind=engine) as db:
            user = db.query(Players).filter(Players.username == username).first()
            print(user.player_id)
            if user.player_id:
                return {"message": "the user already exists"}
            user = Players(username=username, password=password_hash)
            db.add(user)
            db.commit()
            return {"message": "user is create"}
    except Exception as e:
        print(e)


def select_all_users():
    try:
        with Session(autoflush=False, bind=engine) as db:
            users = db.query(Players).order_by(Players.player_id.desc()).all()
        all_users = []
        for user in users:
            all_users.append(
                {
                    'player_id': user.player_id,
                    'username': user.username
                }
            )
        return all_users
    except Exception as e:
        print(e)


def select_user(username):
    try:
        with Session(autoflush=False, bind=engine) as db:
            user = db.query(Players).filter(Players.username == username).first()

            user_data = {
                    'player_id': user.player_id,
                    'username': user.username,
                    'password_hash': user.password
                }
        return user_data
    except Exception as e:
        print(e)
