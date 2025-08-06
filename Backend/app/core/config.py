from pydantic_settings import BaseSettings 

class Settings(BaseSettings):
    DATABASE_URL: str
    GROQ_API_KEY: str = "optional_default"
    GEMINI_API_KEY: str = "optional_default"

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # ADD THIS LINE
    ALPHA_VANTAGE_API_KEY: str
    FINANCIAL_MODELING_PREP_API_KEY: str # <-- ADD THIS

    class Config:
        env_file = ".env"

settings = Settings()