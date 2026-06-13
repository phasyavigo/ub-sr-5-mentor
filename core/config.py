from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MENTOR_LLM_ENDPOINT: str
    MENTOR_LLM_MODEL: str

    class Config:
        env_file = ".env"

settings = Settings()

