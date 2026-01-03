from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    database_url: str = Field(alias="SQLALCHEMY_DATABASE_URL")
    secret_key:str=Field(alias="SECRET_KEY")
    algorithm:str=Field(alias="ALGORITHM")
    expiry_time:int=Field(alias="ACCESS_TOKEN_EXPIRE_MINUTES")

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
