from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.emoji import emojize
import aiosqlite

from config import db_path
from loader import dp


async def give_list():
     
    db = await aiosqlite.connect(db_path)
    cursor = await db.execute('SELECT user_id FROM Users;')
    f_list = await cursor.fetchall()
    result = []
    for i in f_list:
        result.append(i[0])
    await cursor.close()
    await db.close()
    return result


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    name = message['from']['username']
    user_id = message['from']['id']
    he_is_in = user_id in await give_list()
    await message.answer(emojize(f'Привет, {message.from_user.full_name}! Выбери что ты хочешь сделать из кнопок ниже '
                                 f':point_down:'),
                         reply_markup=ReplyKeyboardMarkup(keyboard=[
                             [KeyboardButton(text='Начать')]
                         ], one_time_keyboard=True, resize_keyboard=True))
    if not he_is_in:
        async with aiosqlite.connect(db_path) as db:
            await db.execute('INSERT INTO Users VALUES(NULL,?,?);', (name, user_id))
            await db.commit()