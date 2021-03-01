import uuid
from typing import Optional

from pydantic import BaseModel, Field

class Comment(BaseModel):
	id: str = Field(default_factory=uuid.uuid4, alias="_id")
	#author: Optional[str] = None
	text: str = Field(...)

	class Config:
		allow_population_by_field_name = True
		schema_extra = {
			'example': {
				#'author': 'Author',
				'text': 'Some content'
			}
		}
