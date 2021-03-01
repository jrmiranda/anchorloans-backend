from fastapi_users import models
from pydantic import Field
from typing import Optional

class User(models.BaseUser):
	name: Optional[str] = None

	class Config:
		schema_extra = {
			'name': 'Full Name'
		}


class UserCreate(models.BaseUserCreate):
	name: Optional[str] = None

	class Config:
		schema_extra = {
			'name': 'Full Name'
		}


class UserUpdate(User, models.BaseUserUpdate):
	name: Optional[str] = None
	
	class Config:
		schema_extra = {
			'name': 'Full Name'
		}


class UserDB(User, models.BaseUserDB):
	name: Optional[str] = None

	class Config:
		schema_extra = {
			'name': 'Full Name'
		}