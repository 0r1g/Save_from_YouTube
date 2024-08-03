from pydantic import BaseModel


class TrackBase(BaseModel):
    title: str


class TrackCreate(TrackBase):
    pass


class Track(TrackBase):
    id: int

    class Config:
        from_attributes: True


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    hashed_password: str


class User(UserBase):
    id: int

    class Config:
        from_attributes: True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str
