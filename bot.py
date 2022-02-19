from aiogram import Bot, Dispatcher, executor, types
import logging
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from emoji import emojize
from main import ParseGameInfo
import json
from postgesql import PostgreSQL
import os


TOKEN = '5196205617:AAFsYQ00fo9k8gnAD3UpSFG-zL0HK7-GQOk'

WEBHOOK_HOST = 'https://steam-cracked.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{TOKEN}'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = int(os.environ.get("PORT", 5000))

DB_URI = 'postgres://sbjcleleuacdwv:e6c250d337859f76b5daaed577e8da527c4ce3b3a60aa4dc3abbeeb8674fb069@ec2-52-72-155-37.compute-1.amazonaws.com:5432/d1ndqsjahdoi8v'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

db = PostgreSQL(DB_URI)

@dp.message_handler(commands=['start', 'help'])
async def start(message: types.Message):
    languages = [f'{emojize(":Russia:")} RUS', f'{emojize(":United_Kingdom:")} ENG', f'{emojize(":Ukraine:")} UKR']

    language_select = types.ReplyKeyboardMarkup(resize_keyboard=True)
    language_select.add(*languages)

    await bot.send_message(message.chat.id, 'Please seleck your language: ', reply_markup=language_select)

@dp.message_handler()
async def message(message: types.Message):
    with open('translations.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    result = db.load(message.chat.id)

    if not result:
        db.add_new_user(message.chat.id, 'eng')

    language_change_command = ['🇷🇺 RUS', '🇬🇧 ENG', '🇺🇦 UKR']

    if message.text in language_change_command:
        language_code = message.text.lower().split()[-1]

        db.update_language(language_code, message.chat.id)
        await bot.send_message(message.chat.id, data[language_code]['hi'])
    else:
        parse_info = ParseGameInfo(message.text.lower().split())
        games = parse_info.start()

        language = ''.join(db.get_language(message.chat.id))

        for game in games:
            await bot.send_photo(message.chat.id, game[-1], caption = f"{data[language]['title']}: {game[0]},\n"\
                f"{data[language]['status']}: {game[1]},\n"\
                f"{data[language]['release date']}: {game[2]},\n"\
                f"{data[language]['crack date']}: {game[3]},\n"\
                f"{data[language]['hacker']}: {game[4]},\n")

async def on_startup(dispatcher: Dispatcher) -> None:
    await bot.set_webhook(WEBHOOK_URL)


async def on_shutdown(dp):
    logging.warning('Shutting down..')

    await bot.delete_webhook()

    await dp.storage.close()
    await dp.storage.wait_closed()

    logging.warning('Bye!')

if __name__ == '__main__':
    executor.start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )