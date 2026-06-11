import asyncio
import logging

from aiogram import Bot, Dispatcher
from config import config
from database.database import init_db
from handlers import admin, user


async def main():
    # Настройка логирования для отлова ошибок платежей и сбоев
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    # Инициализация БД
    await init_db()

    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher()

    # Регистрация роутеров
    dp.include_router(user.router)
    dp.include_router(admin.router)

    # Запуск бота (удаляем вебхуки, если были)
    await bot.delete_webhook(drop_pending_updates=True)
    logging.info("Бот успешно запущен!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Бот остановлен.")
