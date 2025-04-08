# this file allows to read our env vars

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL : str

    model_config = SettingsConfigDict(
        env_file = ".env",
        extra="ignore" # prevent extra attributes from creating
    ) 

Config = Settings()