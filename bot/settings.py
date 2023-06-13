from typing import Optional

from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    TOKEN: SecretStr

    POSTGRES_HOST: str
    POSTGRES_PORT: Optional[int]
    POSTGRES_USER: str
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_DB: str

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_USERNAME: str
    REDIS_PASSWORD: SecretStr
    REDIS_DB: int
    IMGBB_API_KEY: SecretStr

    class Config:
        env_file = "stack.env", ".env"
        env_file_encoding = "utf-8"


settings = Settings()
