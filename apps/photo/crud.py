from fastapi import HTTPException
from core.s3 import get_s3_url

not_found_exception = HTTPException(status_code=404, detail='Photo not found')


async def load_photos(db, cond={}):
	photos = []
	async for photo in db.find(cond):
		photo['_id'] = str(photo['_id'])
		photo['url'] = get_s3_url(photo['file_key'], 'photos')
		photos.append(photo)
	return photos


async def verify_photo(db, id):
	photo = await db.find_one({ "_id": id })
	if photo is None:
		raise not_found_exception
	return photo


async def change_photo(db, id, obj):
	update_result = await db.update_one(
		{ "_id": id }, { "$set": obj }
	)
	if update_result.modified_count == 1:
		updated_photo = await db.find_one(
			{ "_id": id }
		)
		return updated_photo

	if (existing_photo := await db.find_one({ "_id": id })) is not None:
		return existing_photo

	raise not_found_exception