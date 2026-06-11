import os

from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: str
    ADMIN_IDS: list[int]
    DB_URL: str = "sqlite+aiosqlite:///shop.db"

    # Добавляем недостающие поля, чтобы Pydantic их не отбрасывал
    YOOKASSA_SHOP_ID: str
    YOOKASSA_SECRET: str
    CRYPTOBOT_TOKEN: str

    # Прямые ссылки на фото (Не забудь заменить на прямые .jpg/.png)
    IMG_MAIN: str = "https://ibb.co/ZpWRSrvg"
    IMG_GAMES: str = "https://ibb.co/KxTqrxCT"
    IMG_SO2: str = "https://ibb.co/KzqBqbKs"
    IMG_BS: str = "https://ibb.co/Rpp0q1pN"
    IMG_PUBG: str = "https://ibb.co/HLHdYS7b"
    IMG_ROBLOX: str = "https://ibb.co/4nqSSgzL"
    IMG_FF: str = "https://ibb.co/ZzBxHWXj"
    IMG_TG: str = "https://ibb.co/ZR72LC1V"
    IMG_PROFILE: str = "https://ibb.co/rRfHwVCf"
    IMG_SERVICES: str = "https://ibb.co/Y7txj2js"
    IMG_BS_GEMS: str = "https://ibb.co/rfQbs9b7"

    # Валидатор, который превратит строку "123,456" или одиночное число "123" в нормальный list[int]
    @field_validator("ADMIN_IDS", mode="before")
    @classmethod
    def parse_admin_ids(cls, v):
        if isinstance(v, str):
            return [int(x.strip()) for x in v.split(",") if x.strip()]
        if isinstance(v, int):
            return [v]
        return v

    class Config:
        env_file = ".env"
        extra = "ignore"  # На всякий случай разрешаем игнорировать лишние параметры


config = Settings()
