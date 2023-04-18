from typing import Optional

from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    TOKEN: SecretStr

    POSTGRES_HOST: str
    POSTGRES_PORT: Optional[int]
    POSTGRES_USER: str
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_DB: str

    class Config:
        env_file = "stack.env", ".env"
        env_file_encoding = "utf-8"


settings = Settings()
