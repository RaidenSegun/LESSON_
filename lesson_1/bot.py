import random
import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from config import token


bot = Bot(token=token)
dp = Dispatcher()


random_number = None




@dp.message(Command('start'))
async def start_command(message: Message):
    await message.answer("Привет! Напиши команду /game, чтобы сыграть в игру.")

@dp.message(Command('game'))
async def start_game(message: Message):
    global random_number
    random_number = random.randint(1, 3)  
    await message.answer("Я загадал число от 1 до 3. Угадайте, какое оно?")

win_image_path = 'C:/Users/User/Desktop/9999/lesson_1/images/win.jpg'
lose_image_path = 'C:/Users/User/Desktop/9999/lesson_1/images/lose.jpg'

@dp.message()
async def guess_number(message: Message):
    global random_number
    if random_number is None:
        await message.answer("Сначала начните игру, ответив командой /game.")
        return

    try:
        user_guess = int(message.text)
        if user_guess == random_number:
            await message.answer("Поздравляю! Вы угадали.")
            if os.path.exists(win_image_path):
                photo = FSInputFile(win_image_path)
                await message.answer_photo(photo, caption="Вы победили!")
            else:
                await message.answer("Изображение победы не найдено.")
            random_number = None  
        else:
            await message.answer("Неправильно. Попробуйте еще раз.")
            if os.path.exists(lose_image_path):
                photo = FSInputFile(lose_image_path)
                await message.answer_photo(photo, caption="Вы проиграли.")
            else:
                await message.answer("Изображение поражения не найдено.")
    except ValueError:
        await message.answer("Пожалуйста, введите число от 1 до 3.")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Бот был остановлен.")