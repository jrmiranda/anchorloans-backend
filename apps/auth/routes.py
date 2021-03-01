from fastapi import FastAPI, Request
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTAuthentication
from fastapi_users.db import MongoDBUserDatabase
from motor.motor_asyncio import AsyncIOMotorClient

from core.config import settings
from .models import User, UserCreate, UserUpdate, UserDB


SECRET_KEY = '61a2cfd5dc47193050d8cd1bf510d94e6f69fabec4e582df573582e54ce8ea7d'


client = AsyncIOMotorClient(settings.DB_URL)
db = client[settings.DB_NAME]
collection = db['users']
user_db = MongoDBUserDatabase(UserDB, collection)


def on_after_register(user: UserDB, request: Request):
	print(f"User {user.id} has registered.")


def on_after_forgot_password(user: UserDB, token: str, request: Request):
	print(f"User {user.id} has forgot their password. Reset token: {token}")


def after_verification_request(user: UserDB, token: str, request: Request):
	print(f"Verification requested for user {user.id}. Verification token: {token}")


jwt_authentication = JWTAuthentication(
	secret=SECRET_KEY, lifetime_seconds=3600, tokenUrl="/auth/jwt/login"
)


fastapi_users = FastAPIUsers(
    user_db,
    [jwt_authentication],
    User,
    UserCreate,
    UserUpdate,
    UserDB,
)