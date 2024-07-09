import uvicorn
from fastapi import FastAPI

from app.api.handlers.auth import register_router, auth_router
from app.api.handlers.recipe import recipe_router

app = FastAPI(docs_url="/")

app.include_router(
    auth_router,
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    register_router,
    prefix="/auth",
    tags=["auth"],
)

app.include_router(recipe_router)

if __name__ == '__main__':
    uvicorn.run('main:app', port=8000, workers=2, log_level="info", reload=True)
