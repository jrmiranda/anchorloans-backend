from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
	username: str
	name: str
	admin: bool = False


class UserInDB(User):
	hashed_password: str


class Token(BaseModel):
	access_token: str
	token_type: str


class TokenData(BaseModel):
	username: Optional[str] = None