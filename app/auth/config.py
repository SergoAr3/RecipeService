from os import getenv
from dotenv import load_dotenv

from fastapi_users.authentication import CookieTransport, JWTStrategy, AuthenticationBackend

cookie_transport = CookieTransport(cookie_name='user_recipe', cookie_max_age=3600)

load_dotenv()


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=getenv('SECRET'), lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)
