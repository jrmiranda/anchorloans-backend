import sys
import os
import uvicorn
from dotenv import load_dotenv
from core.config import settings

# core_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'core')
# sys.path.append(core_path)

load_dotenv()

if __name__ == '__main__':
	uvicorn.run('main:app', host=settings.HOST, port=settings.PORT, reload=settings.DEBUG_MODE)