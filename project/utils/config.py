from pydantic import BaseSettings


class Settings(BaseSettings):
    JWT_SECRET_KEY: str = "e363d9a918ced298f2a4aa68004b04968953210e0e1d8c48"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION: int = 100
    JWT_REFRESH_EXPIRATION: int = 100

    api_prefix: str = "/api/v1"

setting = Settings()