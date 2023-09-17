from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from data.config import ADMINS
from loader import dp, bot


@dp.message_handler(commands=['id'])
async def id_meneger(message: types.Message):
    print(message.from_user.id)
    for admin in ADMINS:
        await bot.send_message(admin, f'Пользователь {message.chat.username}, зарегестрировался его id:{message.from_user.id}')

