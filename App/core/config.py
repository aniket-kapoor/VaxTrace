from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from pathlib import Path

class Settings(BaseSettings):
    database_url: str = Field(alias="SQLALCHEMY_DATABASE_URL")
    secret_key:str=Field(alias="SECRET_KEY")
    algorithm:str=Field(alias="ALGORITHM")
    expiry_time:int=Field(alias="ACCESS_TOKEN_EXPIRE_MINUTES")

    
    storage_root: str = Field(alias="STORAGE_ROOT")
    cloudinary_cloud_name: str = Field(alias="CLOUDINARY_CLOUD_NAME")
    cloudinary_api_key: str = Field(alias="CLOUDINARY_API_KEY")
    cloudinary_api_secret: str = Field(alias="CLOUDINARY_API_SECRET")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def storage_path(self) -> Path:
        """
        Absolute path to storage directory
        """
        return Path(self.storage_root).resolve()


settings = Settings()
