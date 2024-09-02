from pydantic_settings import BaseSettings, SettingsConfigDict
import bcrypt

class Settings(BaseSettings):
    JWT_SECRET: str
    DB_URI: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()

salt = bcrypt.gensalt()