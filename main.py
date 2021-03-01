from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient

from core.config import settings
from apps.photo.routes import router as photo_router
#from apps.auth.routes import router as auth_router

from apps.auth.routes import fastapi_users, jwt_authentication, on_after_register

import sys
import os

core_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'core')
sys.path.append(core_path)

app = FastAPI()

origins = [
	"*" # change
]

app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

# Database
@app.on_event('startup')
async def startup_mongo_client():
	app.mongodb_client = AsyncIOMotorClient(settings.DB_URL)
	app.mongodb = app.mongodb_client[settings.DB_NAME]


@app.on_event('shutdown')
async def shutdown_mongo_client():
	app.mongodb_client.close()


# Routes
app.include_router(fastapi_users.get_auth_router(jwt_authentication), prefix="/auth/jwt", tags=["auth"])
app.include_router(fastapi_users.get_register_router(on_after_register), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_users_router(), prefix="/users", tags=["users"])
app.include_router(photo_router, prefix='/photos', tags=['photos'])
