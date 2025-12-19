from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"
    cors_origins: list[str] = []

    db_url: str = ""
    redis_url: str = ""


settings = Settings()
