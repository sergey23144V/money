from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from handlers.users.mechanic import _connect
from loader import dp


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ("Список команд: ",
            "/start - Начать диалог",
            "/help - Получить справку")
    
    await message.answer("\n".join(text))


@dp.message_handler(commands=['aut'])
async def bot_aut(message: types.Message):
    await _connect(message)