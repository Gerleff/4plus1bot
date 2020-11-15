from asyncio import sleep

import aiosqlite
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ContentType
from aiogram.utils.emoji import emojize
from aiogram.utils.exceptions import TelegramAPIError
from config import admins, db_path
# from keyboards.default.menu import menu

from loader import dp, bot
from states.mailing import Mailing, ToSub, Wait


async def kb_rep(call, text, reply_markup=None, bt=bot):
    try:
        await bt.edit_message_text(chat_id=call.message.chat_id, message_id=call.message.message_id, text=text,
                                   reply_markup=reply_markup)
    except AttributeError:
        await bt.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text,
                                   reply_markup=reply_markup)


def create_kb(lst):
    def create_btn(keb, short):
        btn = InlineKeyboardButton(text=short, callback_data=short)
        keb.insert(btn)

    kb = InlineKeyboardMarkup(row_width=1)
    for i in lst:
        create_btn(kb, i[0])
    return kb


async def give_list():
    db = await aiosqlite.connect(db_path)
    cursor = await db.execute('SELECT user_id FROM Users;')
    f_list = await cursor.fetchall()
    result = [i[0] for i in f_list]
    await cursor.close()
    # print(len(result))
    return result


async def del_from_db(user):
    db = await aiosqlite.connect(db_path)
    await db.execute('DELETE FROM Users WHERE user_id = {};'.format(user))
    await db.commit()
    await db.close()


@dp.callback_query_handler(lambda call: call.data == 'adm_cancel', state=ToSub.Add_Commit)
async def cancel_mails(call: CallbackQuery, state: FSMContext):
    print('прив')
    try:
        await state.reset_state()
    except:
        pass
    await kb_rep(call, 'Ок, если что - пиши "Админка".')


@dp.callback_query_handler(lambda call: call.data == 'adm_cancel', state=ToSub.Add_By_self)
async def cancel_mails(call: CallbackQuery, state: FSMContext):
    print('прив')
    try:
        await state.reset_state()
    except:
        pass
    await kb_rep(call, 'Ок, если что - пиши "Админка".')


@dp.callback_query_handler(lambda call: call.data == 'adm_cancel', state=ToSub.Delete)
async def cancel_mails(call: CallbackQuery, state: FSMContext):
    print('прив')
    try:
        await state.reset_state()
    except:
        pass
    await kb_rep(call, 'Ок, если что - пиши "Админка".')


@dp.callback_query_handler(lambda call: call.data == 'adm_cancel')
async def cancel_mails(call: CallbackQuery, state: FSMContext):
    print('прив')
    try:
        await state.reset_state()
    except:
        pass
    await kb_rep(call, 'Ок, если что - пиши "Админка".')


@dp.callback_query_handler(lambda call: call.data == 'adm_cancel', state=ToSub.Add_Input)
async def cancel_mails(call: CallbackQuery, state: FSMContext):
    print('прив')
    try:
        await state.reset_state()
    except:
        pass
    await kb_rep(call, 'Ок, если что - пиши "Админка".')


@dp.callback_query_handler(lambda call: call.data == 'adm_cancel', state=Mailing.PreMail)
async def cancel_mails(call: CallbackQuery, state: FSMContext):
    print('прив')
    try:
        await state.reset_state()
    except:
        pass
    await kb_rep(call, 'Ок, если что - пиши "Админка".')


@dp.callback_query_handler(lambda call: call.data == 'adm_cancel', state=Mailing.Confirm)
async def cancel_mails(call: CallbackQuery, state: FSMContext):
    print('прив')
    try:
        await state.reset_state()
    except:
        pass
    await kb_rep(call, 'Ок, если что - пиши "Админка".')


@dp.callback_query_handler(lambda call: call.data == 'adm_cancel', state=Mailing.Buttons)
async def cancel_mails(call: CallbackQuery, state: FSMContext):
    print('прив')
    try:
        await state.reset_state()
    except:
        pass
    await kb_rep(call, 'Ок, если что - пиши "Админка".')


@dp.message_handler(lambda message: message.text == emojize('Админка') and message['from']['id'] in admins)
async def admin_in(message: Message):
    admin_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Сколько их уже?', callback_data='users_num'),
         InlineKeyboardButton(text='Рассылка', callback_data='delivery')],
        [InlineKeyboardButton(text='Каналы', callback_data='to_sub')]])
    await message.answer('Добро пожаловать в админку!', reply_markup=admin_kb)


@dp.callback_query_handler(lambda call: call.data == 'users_num')
async def how_many_users(call: CallbackQuery, state: FSMContext):
    try:
        await state.reset_state()
    except:
        pass
    u_list = await give_list()
    await kb_rep(call, 'Их уже аж {}'.format(len(u_list)), reply_markup=InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Рассылка', callback_data='delivery')]]))


@dp.callback_query_handler(lambda call: call.data == 'to_sub')
async def how_many_users(call: CallbackQuery, state: FSMContext):
    try:
        await state.reset_state()
    except:
        pass
    db = await aiosqlite.connect(db_path)
    cursor = await db.execute('SELECT short FROM ToSub;')
    ch_list = await cursor.fetchall()
    await db.close()
    ch_list_new = []
    for i in ch_list:
        ch_list_new.append(i[0])
    await kb_rep(call=call,
                 text='Это меню для добавления/удаления каналов, на которые пользвателю необходимо подписаться, '
                      'чтобы использовать бота\nТекущий список каналов: {}'.format(str(ch_list_new)[1:-1]),
                 reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                     [InlineKeyboardButton(text='Добавить', callback_data='ch_add'),
                      InlineKeyboardButton(text='Удалить', callback_data='ch_delete')],
                     [InlineKeyboardButton(text='Отмена', callback_data='adm_cancel')]
                 ]))


@dp.callback_query_handler(lambda call: call.data == 'ch_delete')
async def delete_ch(call: CallbackQuery, state: FSMContext):
    db = await aiosqlite.connect(db_path)
    cursor = await db.execute('SELECT short FROM ToSub;')
    ch_list = await cursor.fetchall()
    await db.close()
    # print(ch_list)
    await ToSub.Delete.set()
    keyboard = create_kb(ch_list)
    keyboard.add(InlineKeyboardButton(text='Отмена', callback_data='adm_cancel'))
    await kb_rep(call=call, text='Выберите канал для удаления:', reply_markup=keyboard)


@dp.callback_query_handler(state=ToSub.Delete)
async def how_many_users(call: CallbackQuery, state: FSMContext):
    db = await aiosqlite.connect(db_path)
    await db.execute('Delete from tosub where short = ?', (call.data,))
    await db.commit()
    cursor = await db.execute('SELECT short FROM ToSub;')
    ch_list = await cursor.fetchall()
    await db.close()
    keyboard = create_kb(ch_list)
    keyboard.add(InlineKeyboardButton(text='Отмена', callback_data='adm_cancel'))
    await kb_rep(call, text='Выберите канал для удаления:', reply_markup=keyboard)


@dp.callback_query_handler(lambda call: call.data == 'ch_add')
async def how_many_users(call: CallbackQuery, state: FSMContext):
    try:
        await state.reset_state()
    except:
        pass
    await kb_rep(call, text='Перешлите текстовое(!) сообщение из желаемого канала',
                 reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                     [InlineKeyboardButton(text='Ввести данные самому', callback_data='by_self')],
                     [InlineKeyboardButton(text='Отмена', callback_data='adm_cancel')]
                 ]))

    await ToSub.Add_Input.set()


@dp.callback_query_handler(lambda call: call.data == 'by_self', state=ToSub.Add_Input)
async def add_channel(call: CallbackQuery, state: FSMContext):
    await ToSub.Add_By_self.set()
    await kb_rep(call, text='Пришлите данные в формате:\nchannel_id (можно узнать с помощью бота @getmyid_bot)'
                            '\nНазвание канала или короткая ссылка через собачку'
                            '\nCcылку на канал или ссылку-приглашение. Пример: \n\n'
                            '-1001468685415\n'
                            'Лекторий\n'
                            'https://t.me/joinchat/AAAAAFeKXGc7NiKS20H4BA',
                 reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                     [InlineKeyboardButton(text='Отмена', callback_data='adm_cancel')]
                 ]))


@dp.message_handler(state=ToSub.Add_By_self)
async def commit(message: Message, state: FSMContext):
    answer = message.text.split(sep='\n')
    try:
        link, short, ch_id = answer[2], answer[1], answer[0]
    except:
        await message.answer(text='Пришлите данные СТРОГО в соответствии примеру: \n\n'
                                  '-1001468685415\n'
                                  'Лекторий\n'
                                  'https://t.me/joinchat/AAAAAFeKXGc7NiKS20H4BA',
                             reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                 [InlineKeyboardButton(text='Отмена', callback_data='adm_cancel')]
                             ]))
    else:
        try:
            await bot.get_chat_member(ch_id, 717893692)
            db = await aiosqlite.connect(db_path)
            await db.execute('INSERT INTO ToSub (link, short, ch_id) VALUES (?, ?, ?); ', (link, short, ch_id))
            await db.commit()
            await state.reset_state()
            await message.answer(text='Канал успещно добавлен!',
                                 reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                     [InlineKeyboardButton(text='Больше/меньше каналов', callback_data='to_sub')],
                                     [InlineKeyboardButton(text='На этом всё...', callback_data='adm_cancel')]
                                 ]))
        except TelegramAPIError:
            await state.update_data(link=message.text)
            await message.answer(text='Невозможно добавить канал, бот не является его админом. \nПовторите попытку и '
                                      'жмите '
                                      '"Далее".',
                                 reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                     [InlineKeyboardButton(text='Далее', callback_data='bot_admin_check')],
                                     [InlineKeyboardButton(text='Отмена', callback_data='adm_cancel')]
                                 ]))
        except:
            raise


@dp.message_handler(state=ToSub.Add_Input)
async def add_channel(message: Message, state: FSMContext):
    print(message)
    try:
        link = 't.me/' + message['forward_from_chat']['username']
        ch_id = message['forward_from_chat']['id']
        short = '@' + message['forward_from_chat']['username']
        await message.answer(
            text='Добавляем канал, требуемый к подписке со следующими данными:\n' +
                 str(ch_id) + '\n' + link + '\n' + short + '\nПроверьте корректность добавляемого '
                                                           'канала.\n '
                                                           'Добавьте бота в админы канала.',
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Далее', callback_data='bot_admin_check')],
                [InlineKeyboardButton(text='Отмена', callback_data='adm_cancel')]]))
        await state.update_data(link=link, short=short, ch_id=ch_id)
        await ToSub.Add_Commit.set()
    except TypeError:
        short = message['forward_from_chat']['title']
        ch_id = message['forward_from_chat']['id']
        await message.answer(text='Добавляем канал, требуемый к подписке со следующими данными:\n' +
                                  str(ch_id) + '\n' + short +
                                  '\nПроверьте корректность добавляемого канала.\nДобавьте бота в админы '
                                  'канала.\nВведите ссылку-приглашение в качестве подтверждения.',

                             reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                 [InlineKeyboardButton(text='Отмена', callback_data='adm_cancel')]
                             ]))
        await state.update_data(short=short, ch_id=ch_id)
        await ToSub.Add_Commit.set()
    except:
        await message.answer('Пересланное сообщение некорректно. Перешлите текстовое сообщение без вложений и из '
                             'нужного канала.\n' + str(message),
                             reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                 [InlineKeyboardButton(text='Отмена', callback_data='adm_cancel')]
                             ]))
        raise


@dp.callback_query_handler(state=ToSub.Add_Commit)
async def commit(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    link, short, ch_id = data.get("link"), data.get("short"), data.get('ch_id')
    try:
        bot_is_admin = await bot.get_chat_member(ch_id, 717893692)
        print("Труъ")
        db = await aiosqlite.connect(db_path)
        await db.execute('INSERT INTO ToSub (link, short, ch_id) VALUES (?, ?, ?); ', (link, short, ch_id))
        await db.commit()
        await db.close()
        await state.reset_state()
        await bot.send_message(call.message.chat.id, text='Канал успещно добавлен!',
                               reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                   [InlineKeyboardButton(text='Больше/меньше каналов', callback_data='to_sub')],
                                   [InlineKeyboardButton(text='На этом всё...', callback_data='adm_cancel')]
                               ]))
    except TelegramAPIError:
        print("Фолс")
        await kb_rep(call,
                     'Невозможно добавить канал, бот не является его админом. \nПовторите попытку и жмите "Далее".',
                     reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                         [InlineKeyboardButton(text='Далее', callback_data='bot_admin_check')],
                         [InlineKeyboardButton(text='Отмена', callback_data='adm_cancel')]
                     ]))
    except:
        raise


@dp.message_handler(state=ToSub.Add_Commit)
async def commit(message: Message, state: FSMContext):
    data = await state.get_data()
    link, short, ch_id = data.get("link"), data.get("short"), data.get('ch_id')
    try:
        await bot.get_chat_member(ch_id, 717893692)
        print("Труъ")
        db = await aiosqlite.connect(db_path)
        await db.execute('INSERT INTO ToSub (link, short, ch_id) VALUES (?, ?, ?); ', (link, short, ch_id))
        await db.commit()
        await state.reset_state()
        await message.answer(text='Канал успещно добавлен!',
                             reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                 [InlineKeyboardButton(text='Больше/меньше каналов', callback_data='to_sub')],
                                 [InlineKeyboardButton(text='На этом всё...', callback_data='adm_cancel')]
                             ]))
    except TelegramAPIError:
        print("Фолс")
        await state.update_data(link=message.text)
        await message.answer(text='Невозможно добавить канал, бот не является его админом. \nПовторите попытку и жмите '
                                  '"Далее".',
                             reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                 [InlineKeyboardButton(text='Далее', callback_data='bot_admin_check')],
                                 [InlineKeyboardButton(text='Отмена', callback_data='adm_cancel')]
                             ]))
    except:
        raise


@dp.callback_query_handler(lambda call: call.data == 'delivery')
async def start_mailing(call: CallbackQuery):
    await Mailing.PreMail.set()
    await kb_rep(call, text='Пришли или перешли сообщение для рассылки.\n'
                            'Оно будет сразу же разосланно подписчикам.',
                 reply_markup=InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Добавить кнопки', callback_data='add_button')],
        [InlineKeyboardButton(text='Отмена', callback_data='adm_cancel')]
    ]))


@dp.callback_query_handler(lambda call: call.data == 'delivery', state=Mailing.Buttons)
async def start_mailing(call: CallbackQuery):
    await Mailing.PreMail.set()
    await kb_rep(call, text='Пришли или перешли сообщение для рассылки.\n'
                            'Оно будет сразу же разосланно подписчикам.',
                 reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                     [InlineKeyboardButton(text='Добавить кнопки', callback_data='add_button')],
                     [InlineKeyboardButton(text='Отмена', callback_data='adm_cancel')]
                 ]))


@dp.message_handler(state=Mailing.PreMail, content_types=ContentType.ANY)
async def enter_text(message: Message, state: FSMContext):
    try:
        caption = message.caption
    except:
        caption = 'Свяжись с создателем: @gergoltz'
    try:
        data = await state.get_data()
        answer = data.get('markup').split(sep='\n')
        keyboard = InlineKeyboardMarkup()
        row = 0
        for i in answer:
            btn_text = i.split(sep=',,')
            if int(btn_text[0]) > row:
                keyboard.row(InlineKeyboardButton(text=btn_text[1], url=btn_text[2]))
                row += 1
            else:
                keyboard.insert(InlineKeyboardButton(text=btn_text[1], url=btn_text[2]))
    except:
        keyboard = InlineKeyboardMarkup()
    print(message.entities)
    file_id = 'Свяжись с создателем: @gergoltz'
    text = 'Свяжись с создателем: @gergoltz'
    mtype = message.content_type
    if message.reply_markup:
        keyboard = message.reply_markup
    if message.caption_entities:
        caption = message.parse_entities()
    if mtype == ContentType.VIDEO:
        file_id = message.video.file_id
        users = await give_list()
        undelivered = 0
        for user in users:
            try:
                await bot.send_video(video=file_id, chat_id=user, caption=caption, reply_markup=keyboard, parse_mode='HTML')
                await sleep(0.3)
            except:
                undelivered += 1
                await del_from_db(user)
                raise
        await message.answer("Рассылка выполнена. Недоставлено сообщений : {}".format(undelivered))

    elif mtype == ContentType.VIDEO_NOTE:
        file_id = message.video_note.file_id
        users = await give_list()
        undelivered = 0
        for user in users:
            try:
                await bot.send_video_note(video_note=file_id, chat_id=user, reply_markup=keyboard, parse_mode='HTML')
                await sleep(0.3)
            except:
                undelivered += 1
                await del_from_db(user)
                raise
        await message.answer("Рассылка выполнена. Недоставлено сообщений : {}".format(undelivered))

    elif mtype == ContentType.ANIMATION:
        file_id = message.animation.file_id
        users = await give_list()
        undelivered = 0
        for user in users:
            try:
                await bot.send_animation(animation=file_id, chat_id=user, caption=caption, reply_markup=keyboard, parse_mode='HTML')
                await sleep(0.3)
            except:
                undelivered += 1
                await del_from_db(user)
                raise
        await message.answer("Рассылка выполнена. Недоставлено сообщений : {}".format(undelivered))

    elif mtype == ContentType.DOCUMENT:
        file_id = message.document.file_id
        users = await give_list()
        undelivered = 0
        for user in users:
            try:
                await bot.send_document(document=file_id, chat_id=user, caption=caption, reply_markup=keyboard, parse_mode='HTML')
                await sleep(0.3)
            except:
                undelivered += 1
                await del_from_db(user)
                raise
        await message.answer("Рассылка выполнена. Недоставлено сообщений : {}".format(undelivered))

    elif mtype == ContentType.PHOTO:
        file_id = message.photo[-1].file_id
        users = await give_list()
        undelivered = 0
        for user in users:
            try:
                await bot.send_photo(photo=file_id, chat_id=user, caption=caption, reply_markup=keyboard, parse_mode='HTML')
                await sleep(0.3)
            except:
                undelivered += 1
                await del_from_db(user)
                raise
        await message.answer("Рассылка выполнена. Недоставлено сообщений : {}".format(undelivered))

    elif mtype == ContentType.TEXT:
        text = message.text
        if message.entities:
            text = message.parse_entities()
        users = await give_list()
        undelivered = 0
        for user in users:
            try:
                await bot.send_message(chat_id=user, text=text, reply_markup=keyboard, parse_mode='HTML')
                await sleep(0.3)
            except:
                undelivered += 1
                await del_from_db(user)
                raise
        await message.answer("Рассылка выполнена. Недоставлено сообщений : {}".format(undelivered))

    else:
        await message.answer('Этот тип файла не поддерживается. Свяжись с @gergoltz'.format(text),
                             reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                 [InlineKeyboardButton(text='Исправляем', callback_data='delivery_1')],
                                 [InlineKeyboardButton(text='Отмена', callback_data='adm_cancel')]
                             ]))
    await state.reset_state()
    # await Mailing.Confirm.set()


# @dp.callback_query_handler(lambda call: call.data == 'delivery_1', state=Mailing.Confirm)
# async def start_mailing(call: CallbackQuery, state: FSMContext):
# print(call)
#     await Mailing.PreMail.set()
#     await kb_rep(call, 'Пришли новый текст для рассылки', reply_markup=InlineKeyboardMarkup(inline_keyboard=[
#         [InlineKeyboardButton(text='Отмена', callback_data='adm_cancel')]
#     ]))
# await bot.send_message(chat_id=call['from']['id'], text='Пришли новый текст для рассылки')


@dp.callback_query_handler(lambda call: call.data == 'add_button', state=Mailing.PreMail)
async def button_mailing(call: CallbackQuery):
    await bot.send_message(call.message.chat.id,
                           text='Пришли клавиатуру в соответствии примеру:\n'
                                '1,,Кнопка1,,https://www.lamoda.ru/\n'
                                '1,,Кнопка2,,https://www.youtube.com\n'
                                '2,,Кнопка3,,https://vscale.io/\n'
                                '3,,Кнопка4,,https://www.rambler.ru/\n'
                                '3,,Кнопка5,,https://best.aliexpress.ru/\n'
                                '3,,Кнопка6,,https://github.com/',
                           reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                               [InlineKeyboardButton(text='Кнопка1', url='https://www.lamoda.ru/'),
                                InlineKeyboardButton(text='Кнопка2', url='https://www.youtube.com')],
                               [InlineKeyboardButton(text='Кнопка3', url='https://vscale.io/')],
                               [InlineKeyboardButton(text='Кнопка4', url='https://www.rambler.ru/'),
                                InlineKeyboardButton(text='Кнопка5', url='https://best.aliexpress.ru/'),
                                InlineKeyboardButton(text='Кнопка6', url='https://github.com/')],
                               [InlineKeyboardButton(text='Отказаться от кнопок', callback_data='delivery')],
                               [InlineKeyboardButton(text='Отмена', callback_data='adm_cancel')]
                           ]))
    await Mailing.Buttons.set()


@dp.message_handler(state=Mailing.Buttons)
async def button_confirm(message: Message, state: FSMContext):
    try:
        await state.update_data(markup=message.text)
        answer = message.text.split(sep='\n')
        keyboard = InlineKeyboardMarkup()
        row = 0
        for i in answer:
            btn_text = i.split(sep=',,')
            print(i)
            print(btn_text)
            if int(btn_text[0]) > row:
                keyboard.row(InlineKeyboardButton(text=btn_text[1], url=btn_text[2]))
                row += 1
            else:
                keyboard.insert(InlineKeyboardButton(text=btn_text[1], url=btn_text[2]))
    except:
        await message.answer('Пришли в СТРОГОМ соответствии примеру.',
                             reply_markup=InlineKeyboardMarkup([
                                 [InlineKeyboardButton(text='Отказаться от кнопок', callback_data='delivery')],
                                 [InlineKeyboardButton(text='Отмена', callback_data='adm_cancel')]
                             ]))
        raise
    else:
        keyboard.row(InlineKeyboardButton(text='Далее', callback_data='delivery_2'),
                     InlineKeyboardButton(text='Исправить', callback_data='add_button'),
                     InlineKeyboardButton(text='Отказаться от кнопок', callback_data='delivery'),
                     InlineKeyboardButton(text='Отмена', callback_data='adm_cancel'))
        await message.answer(text='Проверьте клавиатуру для добавление в рассылку:', reply_markup=keyboard)


@dp.callback_query_handler(lambda call: call.data == 'delivery_2', state=Mailing.Buttons)
async def start_mailing(call: CallbackQuery):
    await Mailing.PreMail.set()
    await kb_rep(call, text='Пришли сообщение для рассылки.\n'
                            'Оно будет сразу же разослано всем пользователям',
                 reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                     [InlineKeyboardButton(text='Отмена', callback_data='adm_cancel')]
                 ]))


# @dp.callback_query_handler(lambda call: call.data == 'sending_mails', state=Mailing.Confirm)
# async def sending_mails(call: CallbackQuery, state: FSMContext):
#     data = await state.get_data()
#     text = data.get("text")
#     caption, file_id, mtype = data.get("caption"), data.get('file_id'), data.get('mtype')
#     try:
#         answer = data.get('markup').split(sep='\n')
#         keyboard = InlineKeyboardMarkup()
#         row = 0
#         for i in answer:
#             btn_text = i.split(sep=',,')
#             print(i)
#             print(btn_text)
#             if int(btn_text[0]) > row:
#                 keyboard.row(InlineKeyboardButton(text=btn_text[1], url=btn_text[2]))
#                 row += 1
#             else:
#                 keyboard.insert(InlineKeyboardButton(text=btn_text[1], url=btn_text[2]))
#     except:
#         keyboard = None
#     await state.reset_state()
#     users = await give_list()
#     # users = admins
#     # print(await give_list())
#     undelivered = 0
#     for user in users:
#         try:
#             if mtype == ContentType.PHOTO:
#
#             if mtype == ContentType.VIDEO:
#
#             if mtype == ContentType.ANIMATION:
#
#             if mtype == ContentType.DOCUMENT:
#
#             if mtype == ContentType.TEXT:
#
#             await sleep(0.3)
#         except:
#             undelivered += 1
#             await del_from_db(user)
#             raise
#
#     await call.message.answer("Рассылка выполнена. Недоставлено сообщений : {}".format(undelivered))