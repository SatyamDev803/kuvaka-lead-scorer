from pydantic_settings import BaseSettings, SettingsConfigDict

# Defines the application's configuration settings
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    DATABASE_URL: str
    GEMINI_API_KEY: str

settings = Settings()