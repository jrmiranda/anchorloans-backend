import uuid
from typing import Optional

from pydantic import BaseModel, Field

class Photo(BaseModel):
	id: str = Field(default_factory=uuid.uuid4, alias="_id")
	file_key: str = None
	accepted: bool = False
	author: Optional[str] = None

	class Config:
		allow_population_by_field_name = True
		schema_extra = {
			'example': {
				'file_key': 'The photo key',
				'accepted': False
			}
		}


class UpdatePhoto(BaseModel):
	file_key: Optional[str]
	#accepted: Optional[bool]


# def serialize_photo(photo):
# 	return {
# 		"id": photo['_id'],
# 		"url": photo['url']
# 	}