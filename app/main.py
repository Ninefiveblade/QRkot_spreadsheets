from fastapi import FastAPI

from app.core.config import settings
from app.api.routers import main_router
from app.core.init_db import create_first_superuser

app = FastAPI(title=settings.app_title, description=settings.description)
app.include_router(main_router)


@app.on_event('startup')
async def startup():
    await create_first_superuser()


# тут можно отладить запуск просто через python main.py
# для этого нужно убирать абсолютный путь импортов и
# if __name__ == "__main__":
#    uvicorn.run("main:app", host="localhost", port=8000, log_level="info", reload=True)
