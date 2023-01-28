#!/usr/bin/env python3

from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    env_name: str = "Local"
    base_url: str = "http://localhost:8000"
    db_url: str = "sqlite:///./urlshortener.db"

    class Config:
        env_file = ".env"


@lru_cache  # adding settings caching for app speed optimization 
def get_settings() -> Settings:
    settings = Settings()
    print(f"Loading settings for: {settings.env_name} ...")
    return settings


# driver code
if __name__ == "__main__":
    base_settings = get_settings()
    print(base_settings.base_url)
    print(base_settings.db_url)
