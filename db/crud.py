from sqlalchemy.orm import Session
from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(username=user.username, hashed_password=user.hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_track(db: Session, track_id: int):
    return db.query(models.Track).filter(models.Track.id == track_id).first()


def get_all_tracks(db: Session):
    return db.query(models.Track.title).all()


def get_track_by_title(db: Session, title: str):
    return db.query(models.Track).filter(models.Track.title == title).first()


def create_track(db: Session, track: schemas.TrackCreate):
    db_track = models.Track(title=track.title)
    db.add(db_track)
    db.commit()
    db.refresh(db_track)
    return db_track
