from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from config import settings
from apps.photo.routes import router as photo_router
from apps.auth.routes import router as auth_router

app = FastAPI()


# Database
@app.on_event('startup')
async def startup_mongo_client():
	app.mongodb_client = AsyncIOMotorClient(settings.DB_URL)
	app.mongodb = app.mongodb_client[settings.DB_NAME]


@app.on_event('shutdown')
async def shutdown_mongo_client():
	app.mongodb_client.close()


# Routes
app.include_router(auth_router, prefix='/auth', tags=['auth'])
app.include_router(photo_router, prefix='/photos', tags=['photos'])
