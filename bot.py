import logging
from aiogram import Bot, Dispatcher, executor, types
from banshiki import SQbanshik
import random

API_TOKEN = '5119965890:AAGlVxqvhTB9gNCxU8YMixjlSUqByrzI0zc'
# log level
logging.basicConfig(level=logging.INFO)
# bot init
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

db = SQbanshik('database.db')


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer(f"Привет 😉 {message.from_user.full_name} !\nТвой ID : "
                         f"{message.from_user.id}")

    if not db.banshik_exists(message.from_user.id):
        db.add_human(message.from_user.id, message.from_user.full_name)
        await message.answer("Вы добавлены в базу данных !")
    else:
        await message.answer("Такой пользователь уже существует !")

    await message.answer("Помощь /help")


@dp.message_handler(commands=['info'])
async def info(message: types.Message):
    await message.answer(
        "/update_all_bath_house\nОбновить у всех на '?', утром в понедельник, ИЛЬЯ ОБЯЗАТЕЛЬНО !\n\n"
        "/update_all_amount\nОбновить у всех на '0', утром в понедельник, ИЛЬЯ ОБЯЗАТЕЛЬНО !\n\n"
    )


@dp.message_handler(commands=['help'])
async def help_me(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    item1 = types.KeyboardButton('Баня 🍻')
    item2 = types.KeyboardButton('Кто идёт сегодня в баню ? 🏃')
    item3 = types.KeyboardButton('Сдал в кубышку ❓')
    item4 = types.KeyboardButton('Кто, сколько сдал сегодня в кубышку ?')
    item5 = types.KeyboardButton('Веники 🥬')
    item6 = types.KeyboardButton('Всего в кубышке 💰')
    item7 = types.KeyboardButton('Пивная лотерея 🍺 рандом 🎰 от 0 до 15')  # 🎲 💵
    markup.add(item1, item2, item3, item4, item5, item6, item7)
    await message.answer("Выбери одну из функций", reply_markup=markup)


@dp.message_handler(content_types=['text'])
async def lalala(message):
    if message.text == 'Пивная лотерея 🍺 рандом 🎰 от 0 до 15':
        await bot.send_message(message.chat.id, "Выиграл номер : {0}".format(random.randint(0, 15)))
    elif message.text == 'Баня 🍻':
        markup = types.InlineKeyboardMarkup(row_width=2)
        item1 = types.InlineKeyboardButton('да', callback_data='yes')
        item2 = types.InlineKeyboardButton('нет', callback_data='no')
        markup.add(item1, item2)
        await bot.send_message(message.chat.id, "Пойдёшь сегодня в баню ?", reply_markup=markup)
    elif message.text == 'Сдал в кубышку ❓':
        markup = types.InlineKeyboardMarkup(row_width=4)
        item1 = types.InlineKeyboardButton('0', callback_data='0')
        item2 = types.InlineKeyboardButton('50', callback_data='50')
        item3 = types.InlineKeyboardButton('100', callback_data='100')
        item4 = types.InlineKeyboardButton('150', callback_data='150')
        markup.add(item1, item2, item3, item4)
        await bot.send_message(message.chat.id, "Сколько ты сегодня сдал в кубышку ?", reply_markup=markup)
    elif message.text == 'Кто идёт сегодня в баню ? 🏃':
        await message.answer(f"Вот кто идёт сегодня в баню :\n\n {db.get_bath()}")
    elif message.text == 'Кто, сколько сдал сегодня в кубышку ?':
        await message.answer(f"Сегодня сдали :\n\n {db.get_amount()}")
    elif message.text == '/update_all_bath_house':
        await message.answer("Обновил 🤝")
        db.update_everyone_bath_house('?')
    elif message.text == '/update_all_amount':
        await message.answer("Обновил 🤝")
        db.update_everyone_amount(0)

    elif message.text == 'Веники 🥬':
        markup = types.InlineKeyboardMarkup(row_width=3)
        item1 = types.InlineKeyboardButton('50', callback_data='fifty')
        item2 = types.InlineKeyboardButton('100', callback_data='one_hundred')
        item3 = types.InlineKeyboardButton('300', callback_data='300')
        markup.add(item1, item2, item3)
        await bot.send_message(message.chat.id, "Сколько взяли на веники ?", reply_markup=markup)

    elif message.text == 'Всего в кубышке 💰':
        await message.answer(f"Всего в кубышке :\n {db.get_kubyshka()} монеток")


@dp.callback_query_handler(lambda callback_query: True)
async def some_callback_handler(callback_query: types.CallbackQuery):
    if callback_query.message:
        if callback_query.data == 'yes':
            db.update_bath('да', callback_query.from_user.id)
        elif callback_query.data == 'no':
            db.update_bath('нет', callback_query.from_user.id)
            # await bot.send_message(callback_query.message.chat.id, "Записал 😉")
        elif callback_query.data == '0':
            db.update_amount(0, callback_query.from_user.id)
            db.add_kubyshka(0)
        elif callback_query.data == '50':
            db.update_amount(50, callback_query.from_user.id)
            db.add_kubyshka(50)
        elif callback_query.data == '100':
            db.update_amount(100, callback_query.from_user.id)
            db.add_kubyshka(100)
        elif callback_query.data == '150':
            db.update_amount(150, callback_query.from_user.id)
            db.add_kubyshka(150)
        elif callback_query.data == 'fifty':
            db.delete_kubyshka(50)
        elif callback_query.data == 'one_hundred':
            db.delete_kubyshka(100)
        elif callback_query.data == '300':
            db.delete_kubyshka(300)
        await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                    message_id=callback_query.message.message_id, text="Записал 😉")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
