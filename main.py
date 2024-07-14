import uvicorn
from fastapi import FastAPI

from app.api.handlers.recipe import recipe_router
from app.auth.handlers import auth_router

app = FastAPI(docs_url="/")

app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    recipe_router,
    prefix="/recipe",
    tags=["Recipe"],
)

if __name__ == '__main__':
    uvicorn.run('main:app', port=8000, workers=2, log_level="info", reload=True)
