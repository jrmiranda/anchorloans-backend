from fastapi import APIRouter, HTTPException, Depends, Body, Request, File, UploadFile, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from .models import Photo, UpdatePhoto
from ..auth.models import User
from ..auth.routes import fastapi_users
from ..comment.models import Comment
from core.s3 import upload_to_s3, get_s3_url

from .crud import load_photos, change_photo, verify_photo

router = APIRouter()


# @router.post("/file-upload")
# async def upload(file: UploadFile = File(...)):
# 	bad_request = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid file')
# 	if file.content_type.split('/')[0] != 'image':
# 		raise bad_request
# 	photo = Photo()
# 	photo.file_key = str(photo.id) + '.' + file.content_type.split('/')[1]
# 	return photo


# @router.post('/test')
# async def testpost(user: User = Body(...)):
# 	return user


@router.post('/')
async def create_photo(
	request: Request,
	user: User = Depends(fastapi_users.current_user()),
	file: UploadFile = File(...)
):
	# check if file is ok
	mimetype, ext = file.content_type.split('/')

	if mimetype != 'image':
		raise HTTPException(status_code=404, detail='Invalid format')

	# create object
	photo = Photo()
	photo.file_key = f'{str(photo.id)}.{ext}'

	# upload
	upload_obj = upload_to_s3(file.file, photo.file_key, 'photos')

	# set user
	photo = jsonable_encoder(photo)
	photo['user_id'] = str(user.id)

	new_photo = await request.app.mongodb['photos'].insert_one(photo)
	created_photo = await request.app.mongodb['photos'].find_one(
		{ "_id": str(new_photo.inserted_id) }
	)
	return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_photo)


@router.get('/')
async def list_photos(request: Request):
	photos = await load_photos(request.app.mongodb['photos'], { "accepted": True })
	return photos


@router.get('/pending')
async def list_pending_photos(request: Request, user: User = Depends(fastapi_users.current_user(active=True, superuser=True))):
	photos = await load_photos(request.app.mongodb['photos'], { "accepted": False })
	return photos


@router.get('/{photo_id}')
async def get_photo(request: Request, photo_id: str):
	photo = await verify_photo(request.app.mongodb['photos'], photo_id)
	photo['url'] = get_s3_url(photo['file_key'], 'photos')
	return photo


@router.put('/{photo_id}')	
async def update_photo(request: Request, photo_id: str, photo: UpdatePhoto = Body(...)):
	photo = {k: v for k,v in photo.dict().items() if v is not None}
	update_result = await change_photo(request.app.mongodb['photos'], photo_id, photo)
	return update_result


@router.delete('/{photo_id}')
async def delete_photo(request: Request, photo_id: str):
	delete_result = await request.app.mongodb['photos'].delete_one(
		{ "_id": photo_id }
	)

	if delete_result.deleted_count == 1:
		return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

	raise HTTPException(status_code=404, detail='Photo not found')
	

@router.post('/{photo_id}/comment')
async def create_comment(
	photo_id: str,
	request: Request,
	comment: Comment = Body(...),
	user: User = Depends(fastapi_users.current_user())
):
	photo = await verify_photo(request.app.mongodb['photos'], photo_id)
	comment = jsonable_encoder(comment)
	comment['author'] = user.name
	update_result = await request.app.mongodb['photos'].update_one(
		{ "_id": photo_id }, { "$push": { "comments": comment } }
	)
	return comment


@router.get('/{photo_id}/accept')
async def accept_photo(
	photo_id: str,
	request: Request,
	user: User = Depends(fastapi_users.current_user(active=True, superuser=True))
):
	db = request.app.mongodb['photos']
	update_result = await change_photo(db, photo_id, { "accepted": True })
	return update_result


@router.get('/{photo_id}/reject')
async def reject_photo(
	photo_id: str,
	request: Request,
	user: User = Depends(fastapi_users.current_user(active=True, superuser=True))
):
	db = request.app.mongodb['photos']
	update_result = await change_photo(db, photo_id, { "accepted": False })
	return update_result


# @router.post('/{photo_id}/accept')
# async def accept_photo(
# 	photo_id: str,
# 	request: Request,
# 	user: User = Depends(fastapi_users.current_user())
# ):
# 	photo = await request.app.mongodb['photos'].find_one({ "_id": photo_id })
# 	if photo is None:
# 		raise HTTPException(status_code=404, detail='Photo not found')

# 	update_result = await request.app.mongodb['photos'].update_one(
# 		{ "_id": photo_id }, { "$set": { "accepted": True } }
# 	)

# 	return photo