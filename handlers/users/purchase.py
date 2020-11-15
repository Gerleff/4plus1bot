import asyncio
from random import randint
import aiosqlite
from aiogram.dispatcher import FSMContext
from fuzzywuzzy import process
from aiogram.types import Message, CallbackQuery, ChatActions, InlineKeyboardMarkup, InlineKeyboardButton, ContentType, \
    ParseMode
from aiogram.utils.emoji import emojize, demojize
import logging
from config import admins, db_path, bot_id, film_list_text
from loader import dp, bot
from states.mailing import Wait


async def sub_filter(message):
    result = True
    db = await aiosqlite.connect(db_path)
    cursor = await db.execute('SELECT short FROM ToSub;')
    ch_list = await cursor.fetchall()
    await db.close()
    ch_list_new = []
    for i in ch_list:
        ch_list_new.append(i[0])
    for i in ch_list_new:
        verse = await bot.get_chat_member(i, message.from_user.id)
        # print(verse)
        result = verse.is_chat_member()
        # print(result)
        if not result:
            break
    return result


async def kb_rep(call, text, reply_markup=None, bt=bot):
    try:
        await bt.edit_message_text(chat_id=call.message.chat_id, message_id=call.message.message_id+1, text=text,
                                   reply_markup=reply_markup,
                                   parse_mode='HTML',
                                   disable_web_page_preview='True')
    except AttributeError:
        await bt.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id+1, text=text,
                                   reply_markup=reply_markup,
                                   parse_mode='HTML',
                                   disable_web_page_preview='True')


def create_kb(lst):
    def create_btn(keb, name, id):
        btn = InlineKeyboardButton(text=name, callback_data=id)
        keb.insert(btn)

    kb = InlineKeyboardMarkup(row_width=1)

    for i in lst:
        create_btn(kb, i[0], i[1])
    return kb


async def sub_keb():
    def create_kb_sub(lst):
        def create_btn(keb, short, link):
            btn = InlineKeyboardButton(text=emojize('Подписаться на канал {} ↗️'.format(short)), url=link)
            keb.insert(btn)

        kb = InlineKeyboardMarkup(row_width=1)
        for i in range(len(lst)):
            create_btn(kb, i + 1, lst[i][1])
        return kb

    db = await aiosqlite.connect(db_path)
    cursor = await db.execute('SELECT short, link FROM ToSub;')
    ch_list = await cursor.fetchall()
    await db.close()
    keyboard = create_kb_sub(ch_list)
    keyboard.add(InlineKeyboardButton(text=emojize('Я подписался(ась) :heart:'), callback_data='subbed'))
    return keyboard


async def sub_txt():
    db = await aiosqlite.connect(db_path)
    cursor = await db.execute('SELECT short, link FROM ToSub;')
    ch_list = await cursor.fetchall()
    await db.close()
    text = '❌ <b>ДОСТУП ЗАКРЫТ</b> ❌\n\n' \
           '👉Для доступа к приватному каналу нужно быть подписчиком ' \
           '<b>Кино-каналов.</b>\n ' \
           'Подпишись на каналы ниже 👇 и нажми кнопку\n' \
           '<b>Я ПОДПИСАЛСЯ</b> для проверки!\n'
    for i in range(len(ch_list)):
        text += '\n<a href={}>Канал {}</a> - {}'.format(ch_list[i][0], i+1, ch_list[i][1])
    return text


@dp.message_handler(lambda message: demojize(message.text) == film_list_text
                                    or demojize(message.text) == demojize("🗄 Список фильмов"))
async def show_film_list(message: Message):
    sub_check = await sub_filter(message)
    if sub_check is True:
        pass
    else:
        pass


@dp.callback_query_handler(lambda call: call.data == 'btn1')
async def show_list(call: CallbackQuery):
    text = await sub_txt()
    await bot.send_message(chat_id=call.message.chat.id,
                           text=emojize(text),
                           parse_mode='HTML',
                           disable_web_page_preview='True',
                           reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                               [InlineKeyboardButton(text=emojize('🥤Я ПОДПИСАЛСЯ🥤'), callback_data='btn2')]
                           ]))


@dp.callback_query_handler(lambda call: call.data == 'btn2')
async def show_list(call: CallbackQuery, state: FSMContext):
    await bot.send_message(chat_id=call.message.chat.id,
                           text=emojize('⏳ Ожидайте 20 сек. Идёт проверка подписки.'),
                           parse_mode='HTML')
    await Wait.Wait.set()
    await bot.send_chat_action(call.from_user.id, ChatActions.TYPING)
    await asyncio.sleep(15)
    subbed = await sub_filter(call)
    if subbed:
        await kb_rep(call, 'Krasava epta', reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Go to archive', url='t.me/kek')]
        ]))
    else:
        text = await sub_txt()
        await kb_rep(call,
                     emojize(text),
                     reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                         [InlineKeyboardButton(text=emojize('🥤Я ПОДПИСАЛСЯ🥤'), callback_data='btn2')]
                     ]))
    await state.reset_state()


@dp.message_handler()
async def show_film_list(message: Message):
    await message.answer(emojize('🥤<b>Все новинки фильмов 2020 доступны на нашем приватном канале.</b>'
                                 '\n📲<b>Приятного просмотра</b> 👇👇👇'),
                         parse_mode='HTML',
                         reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                             [InlineKeyboardButton(text=emojize('🥤НАЧАТЬ СМОТРЕТЬ🥤'), callback_data='btn1')]
                         ]))
