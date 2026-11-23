from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    API_ID: int
    API_HASH: str

    model_config = SettingsConfigDict(env_file="config/.env",extra="ignore")

settings = Settings()