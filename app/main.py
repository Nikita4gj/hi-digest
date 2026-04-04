from fastapi import FastAPI
from app.core.lifespan import lifespan
from app.api.routes.stories import router as story_router

from app.models import Story

#* Создание приложения
app = FastAPI(lifespan=lifespan)

app.include_router(story_router)




