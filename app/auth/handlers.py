from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from app.auth.utils import validate_auth_user, encode_jwt
from app.services.auth import AuthService
from app.schemas.token import Token
from app.schemas.user import UserCreate

import app.api.constants.status_codes as status_codes


auth_router = APIRouter()


@auth_router.post('/register', status_code=status.HTTP_201_CREATED)
async def register(
        user: UserCreate,
        auth_service: Annotated[AuthService, Depends()],
):
    await auth_service.create_user_db(user)
    return status_codes.HTTP_200_OK_register


@auth_router.post('/login', response_model=Token)
async def login_access_token(
        user: UserCreate = Depends(validate_auth_user)
):
    jwt_payload = {
        'sub': user.username,
        'username': user.username,
    }
    token = await encode_jwt(jwt_payload)
    return Token(
        access_token=token,
        token_type="Bearer"
    )
