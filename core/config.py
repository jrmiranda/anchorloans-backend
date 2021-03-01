import os
from pydantic import BaseSettings


class CommonSettings(BaseSettings):
	APP_NAME: str = 'Wedbook'
	DEBUG_MODE: bool = True


class ServerSettings(BaseSettings):
	HOST: str = '0.0.0.0'
	PORT: int = 8000


class DatabaseSettings(BaseSettings):
	DB_URL: str = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
	DB_NAME: str = 'wedbook'


class Settings(CommonSettings,ServerSettings,DatabaseSettings):
	class Config:
		env_file = ".env"


settings = Settings()