from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env')
    
    APP_NAME: str
    REDIS_HOST: str
    REDIS_PORT: str


config = Config()
