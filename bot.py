import json
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


TOKEN = '8083159938:AAGgGgd3qCaKl3JbQDha6Tvpbfr5pqPSGnI'

# Загрузка вопросов из файла
def load_questions():
    with open('questions.json', 'r', encoding='utf-8') as f:
        return json.load(f)

questions = load_questions()


user_data = {}

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())


@dp.message(Command("start"))
async def start(message: Message):
    user_id = message.from_user.id
    user_data[user_id] = {'score': 0, 'question_index': 0}
    await message.answer("Привет! Я бот-викторина. Напиши /victorina, чтобы начать игру.")


@dp.message(Command("victorina"))
async def victorina(message: Message):
    user_id = message.from_user.id
    if user_id not in user_data:
        await message.answer("Сначала напиши /start, чтобы начать игру.")
        return

    question_index = user_data[user_id]['question_index']
    if question_index >= len(questions):
        await message.answer(f"Игра окончена! Ваш результат: {user_data[user_id]['score']} из {len(questions)}.")
        del user_data[user_id]
        return

    question = questions[question_index]
    options = '\n'.join([f"{i+1}. {ans}" for i, ans in enumerate(question['answers'])])
    await message.answer(f"Вопрос {question_index + 1}: {question['question']}\n{options}")


@dp.message()
async def handle_answer(message: Message):
    user_id = message.from_user.id
    if user_id not in user_data:
        return

    question_index = user_data[user_id]['question_index']
    if question_index >= len(questions):
        return

    question = questions[question_index]
    try:
        answer_index = int(message.text) - 1
        if 0 <= answer_index < len(question['answers']):
            if answer_index == question['correct']:
                user_data[user_id]['score'] += 1
            user_data[user_id]['question_index'] += 1
            await victorina(message)
        else:
            await message.answer("Пожалуйста, отправьте номер ответа.")
    except ValueError:
        await message.answer("Пожалуйста, отправьте номер ответа.")


async def main():
    await dp.start_polling(bot)

if __name__ == 'main':
    asyncio.run(main())