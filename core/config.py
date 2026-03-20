from dotenv import load_dotenv
from pydantic_settings import BaseSettings
import pathlib

load_dotenv()

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent


class AuthSettings(BaseSettings):
    ALGORITHM: str = "RS256"

    PRIVATE_KEY: pathlib.Path = BASE_DIR / "certs" / "private_jwt.pem"
    PUBLIC_KEY: pathlib.Path = BASE_DIR / "certs" / "public_jwt.pem"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


class Settings(BaseSettings):
    db_url: str = f"sqlite+aiosqlite:///{BASE_DIR}/db.sqlite3"
    db_echo: bool = False

    AuthSettings()


settings = Settings()
auth_settings = AuthSettings()