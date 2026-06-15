from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    ollama_host: str = "http://localhost:11434"
    ollama_default_model: str = "llama3.1:8b"
    allowed_origins: list[str] = ["http://localhost:4200"]
    lamp_count: int = 12
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="APP_",
        extra="ignore",
    )
settings = Settings()