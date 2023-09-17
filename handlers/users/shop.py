from aiogram import types
from aiogram.types import InlineKeyboardButton

from loader import dp, bot



# def webAppKeyboard(): #создание клавиатуры с webapp кнопкой
#    keyboard = types.ReplyKeyboardMarkup(row_width=1) #создаем клавиатуру
#    webAppTest = types.WebAppInfo(url=" https://751f-178-76-226-239.ngrok-free.app/shop/") #создаем webappinfo - формат хранения url
#    one_butt = types.KeyboardButton(text="Тестовая страница", web_app=webAppTest) #создаем кнопку типа webapp
#    keyboard.add(one_butt) #добавляем кнопки в клавиатуру
#
#    return keyboard #возвращаем клавиатуру
#


async def Shop():
   keyboard = types.InlineKeyboardMarkup()

   keyboard.add(types.InlineKeyboardButton(text="Розыгрышь", callback_data="entrance"),)
   keyboard.add(types.InlineKeyboardButton('Обучение', callback_data="entrance"),types.InlineKeyboardButton('Техника', callback_data="entrance"))
   keyboard.add(types.InlineKeyboardButton('Электр. товары', callback_data="entrance"), types.InlineKeyboardButton('Книги', callback_data="entrance"))
   keyboard.add(types.InlineKeyboardButton('Назад', callback_data="entrance"), types.InlineKeyboardButton('⚠️Правила', callback_data="entrance"))

   return keyboard


async def Back():
   keyboard = types.InlineKeyboardMarkup()

   keyboard.add(types.InlineKeyboardButton('Назад', callback_data="menu"))

   return keyboard

@dp.callback_query_handler(text="shop")
async def settings(call: types.CallbackQuery):
   keyboard = await Back()
   # await bot.send_message(call.message.chat.id, 'Привет, я бот для проверки телеграмм webapps!)',reply_markup=Shop())
   await bot.send_message(call.message.chat.id, 'Прошу прощения, пока эта функция на доработке',reply_markup= keyboard)
