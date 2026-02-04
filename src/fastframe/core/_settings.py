from pathlib import Path

from pydantic_settings import BaseSettings as _BaseSettings


class Settings(_BaseSettings):
    @property
    def fastframe_base_dir(self) -> Path:
        return Path(__file__).parent.parent.parent.parent


settings: Settings = Settings()


class BaseSettings(_BaseSettings):
    pass
