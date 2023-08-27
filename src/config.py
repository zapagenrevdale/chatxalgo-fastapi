from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "ChatXAlgo"
    token_algorithm: str
    token_secret_key: str
    token_expire_minutes: int

    model_config = SettingsConfigDict(env_file=".env")
