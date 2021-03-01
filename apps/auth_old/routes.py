from fastapi import APIRouter, HTTPException, Body, Request, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

#from jose import JWTError, jwt
from .security import verify_password, get_password_hash
from .models import User, UserInDB


SECRET_KEY = '61a2cfd5dc47193050d8cd1bf510d94e6f69fabec4e582df573582e54ce8ea7d'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


router = APIRouter()


async def get_current_user(token: str = Depends(oauth2_scheme)):
	return User(username='Jr', name='Jr Miranda')


@router.post('/')
async def create_user(request: Request, user: User = Body(...)):
	user = jsonable_encoder(user)
	new_user = await request.app.mongodb['users'].insert_one(user)
	created_user = await request.app.mongodb['users'].find_one(
		{ "_id": str(new_user.inserted_id) }
	)
	return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_user)


@router.post('/token')
async def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
	# check user
	user = await request.app.mongodb['users'].find_one({ "username": form_data.username })
	
	

	if user is None:
		raise HTTPException(status_code=400, detail='user not found')
	
	return { "access_token": user['username'], "token_type": "bearer" }


@router.get('/me')
async def user_me(current_user: User = Depends(get_current_user)):
	return current_user

