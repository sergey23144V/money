import logging

from aiogram import Dispatcher

from data.config import ADMINS
from loader import dp


async def on_startup_notify(dp: Dispatcher):
    admins = ADMINS
    try:
        for admin in admins:
            await dp.bot.send_message(admin, "Бот Запущен")

    except Exception as err:
        logging.exception(err)
