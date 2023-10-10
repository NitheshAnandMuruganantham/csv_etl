from fastapi import FastAPI
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    REDIS_URL: str
    REDIS_PORT: int
    REDIS_PASSWORD: str
    AWS_REGION_NAME: str
    MONGO_URL: str
    AUTH_SECRET: str
    ENV: str
    AUTH_ALGORITHM: str
    TWILIO_ACCOUNT_SID: str
    TWILIO_AUTH_TOKEN: str
    RABITMQ_URL: str
    TWILIO_PHONE_NUMBER: str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    DATABASE_URL: str
    SENDINBLUE_API_KEY: str
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()
