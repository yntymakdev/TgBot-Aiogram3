import asyncio
import logging
import sys
from os import getenv
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
import os

# Загружаем токен из переменной окружения
TOKEN = os.getenv("TELEGRAM_TOKEN")

# Настроим логирование
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

# Инициализируем бота
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

# Инициализируем диспетчер
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    Этот хендлер обрабатывает команду /start
    """
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")


@dp.message()
async def echo_handler(message: Message) -> None:
    """
    Этот хендлер отправляет обратно полученное сообщение
    """
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Nice try!")


async def main() -> None:
    # Запуск polling
    await dp.start_polling(bot)


if __name__ == "__main__":
    # Запуск основного процесса
    asyncio.run(main())
    