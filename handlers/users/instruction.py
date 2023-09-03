from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from data.config import ADMINS
from handlers.users.start import user_username, id_user
from loader import dp, bot


async def instruction(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Далее 1 из 3", callback_data="instruction1"))
    await bot.send_photo(chat_id=message.chat.id,
                         photo="https://downloader.disk.yandex.ru/preview/0ecb4e3ac44ed45551f4dddeede596a2ac1ff73d8e8dede6cb05d4061cef7519/641b2f71/YLl_0Fu4csCERoyCuarUVt4sDjQKomanFhLx_E_BiQnQzY6pc93X19kYCvGDYVNjsRZMHOc6zYCdIgqliU5JOg%3D%3D?uid=0&filename=Стартовая%20картинка%20после%20запуска.png&disposition=inline&hash=&limit=0&content_type=image%2Fpng&owner_uid=0&tknv=v2&size=1855x947",
                         caption="ВНИМАНИЕ! Посмотрите инструкцию!\n\n"
                                 "При входе в модуль обмена оценок на рубли вы видите текущий курс обмена оценок.\n\n"
                                 "Кнопка 'обменять оценки' запустит модуль обмена оценок.\n\n"
                                 "Кнопка 'Пока нет оценок' вернет вас обратно.\n\n"
                                 "Кнопка 'Увеличить курс в 2 раза' перенаправит вас в модуль подписки.",

                         reply_markup=keyboard)


@dp.callback_query_handler(text="instruction1")
async def instruction1(call: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Далее 2 из 3", callback_data="instruction2"))
    await bot.send_photo(chat_id=call.message.chat.id,
                         photo="https://downloader.disk.yandex.ru/preview/0ecb4e3ac44ed45551f4dddeede596a2ac1ff73d8e8dede6cb05d4061cef7519/641b2f71/YLl_0Fu4csCERoyCuarUVt4sDjQKomanFhLx_E_BiQnQzY6pc93X19kYCvGDYVNjsRZMHOc6zYCdIgqliU5JOg%3D%3D?uid=0&filename=Стартовая%20картинка%20после%20запуска.png&disposition=inline&hash=&limit=0&content_type=image%2Fpng&owner_uid=0&tknv=v2&size=1855x947",
                         caption='Выбери, какую оценку ты хочешь обменять, просто нажми на одну из цифр. Если нет оценок,'
                                 ' нажми "Назад" и возвращайся, когда у тебя появятся оценки для обмена.',
                         reply_markup=keyboard)


@dp.callback_query_handler(text="instruction2")
async def instruction2(call: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Далее 3 из 3", callback_data="menu"))
    await bot.send_photo(chat_id=call.message.chat.id,
                         photo="https://downloader.disk.yandex.ru/preview/0ecb4e3ac44ed45551f4dddeede596a2ac1ff73d8e8dede6cb05d4061cef7519/641b2f71/YLl_0Fu4csCERoyCuarUVt4sDjQKomanFhLx_E_BiQnQzY6pc93X19kYCvGDYVNjsRZMHOc6zYCdIgqliU5JOg%3D%3D?uid=0&filename=Стартовая%20картинка%20после%20запуска.png&disposition=inline&hash=&limit=0&content_type=image%2Fpng&owner_uid=0&tknv=v2&size=1855x947",
                         caption='В этом месте вам необходимо отправить фотографию оценки. Нажмите на скрепку, сфотографируйте оценку или выберите ее из галереи. Если не планируете отправлять оценку, нажмите "назад".',
                         reply_markup=keyboard)
