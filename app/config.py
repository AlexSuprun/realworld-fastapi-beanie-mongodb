from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "mongodb://localhost:27017/conduit?directConnection=true"
    secret: str = "your-jwt-secret-key"
    algorithm: str = "HS256"
    access_token_expire_hours: int = 5

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
