from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    TOKEN: SecretStr

    class Config:
        env_file = "stack.env", ".env"
        env_file_encoding = "utf-8"


settings = Settings()
