from aiogram import types

from loader import dp, bot

id_user = ''
user_username = ''


users = 407899


async def count_user():
    global users
    users += 1
    return f"{users}"


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    global id_user, user_username

    id_user = message.from_user.id
    user_username = message.from_user.username

    nameuser = message.from_user.username
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Подключиться к программе", callback_data="acquaintance1"))

    await bot.send_photo(chat_id=message.chat.id, photo="https://downloader.disk.yandex.ru/preview/0ecb4e3ac44ed45551f4dddeede596a2ac1ff73d8e8dede6cb05d4061cef7519/641b2f71/YLl_0Fu4csCERoyCuarUVt4sDjQKomanFhLx_E_BiQnQzY6pc93X19kYCvGDYVNjsRZMHOc6zYCdIgqliU5JOg%3D%3D?uid=0&filename=Стартовая%20картинка%20после%20запуска.png&disposition=inline&hash=&limit=0&content_type=image%2Fpng&owner_uid=0&tknv=v2&size=1855x947",
                         caption="Привет,@" + nameuser + "\nДобро пожаловать в федеральную программу 'Деньги за "
                                                         "оценки' от компании Sokrat!\n\n Для чего нужна эта "
                                                         "программа?\n\n 1️⃣  Мы хотим поддержать тебя и позволить в "
                                                         "будущем сэкономить на образовании\n2️⃣  " +
                                 "А еще хотим стимулировать тебя получать как можно больше хороших оценок, тем самым "
                                 "улучшить твою успеваемость в школе!\n3️⃣ Онлайн - поступление в лучшие ВУЗы и ССУЗы России"
                                 "\n4️⃣ Приобретай товары в школьном магазине. \n\n👤  "
                                + str(users) +" участников",
                         reply_markup=keyboard)