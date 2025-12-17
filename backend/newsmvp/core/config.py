from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"
    db_url: str = ""

    cors_origins: list[str] = []


settings = Settings()
