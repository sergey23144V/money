from datetime import datetime
import requests
from aiogram import types
from aiogram.dispatcher import FSMContext
from telebot.callback_data import CallbackData
from states.ClassUser import User
from data.config import ADMINS
from handlers.users.mechanic import menu
from handlers.users.start import user_username
from loader import dp, bot

cb = CallbackData('action', prefix='keyboard')

listUniv = {'Заведение': 1}


@dp.callback_query_handler(text="entrance")
async def entrance(call: types.CallbackQuery, state: FSMContext):
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text="Выбрать ВУЗ", callback_data="UNIVERSITY")
    button2 = types.InlineKeyboardButton(text="Назад", callback_data="menu")
    keyboard.row(button1)
    keyboard.row(button2)
    await bot.send_photo(chat_id=call.message.chat.id,
                         photo="https://downloader.disk.yandex.ru/preview/2c9d6195fe98b386fd8540c15d602b1317bca79f8a3a59b5762170f211982e7c/642d780e/Kh-Qn5DFYEbHzwNGp49Ky0r9N2DqxgbnVTwuaGpxRfbQL9_zVXCWPArtRDZ4DQq2P1Lj_grgMww07gcjAV4_PA%3D%3D?uid=0&filename=Картинка%206.png&disposition=inline&hash=&limit=0&content_type=image%2Fpng&owner_uid=0&tknv=v2&size=1855x947",
                         caption="Serega_4, поступите в один из университетов со скидкой от Sokrat.\n\n"
                              "Sokrat - это:\n- Бесплатная консультация\n- Подача документов онлайн\n"
                              "- Подбор ВУЗа бесплатно\n- Выгодные условия поступления\n- Поступление без ЕГЭ*\n\n"
                              "*Действует не на все учебные заведения - партнеры Sokrat",
                         reply_markup=keyboard)
    data = await state.get_data()
    email = data.get('user_email')
    await bot.send_message(ADMINS, f"Пользователь {email} перешел в онлайн поступления")


@dp.callback_query_handler(text="UNIVERSITY")
async def UNIVERSITY(call: types.CallbackQuery,state: FSMContext):
    global listUniv
    keyboard = types.ReplyKeyboardMarkup()
    txt = f"Выберете один из учебных заведений:\n"
    txt = await get_unev(keyboard=keyboard, listUniv=listUniv, txt=txt)

    await call.message.answer(txt, reply_markup=keyboard)
    await User.univ.set()


@dp.message_handler(state=User.univ)
async def choice_unev(message: types.Message,state: FSMContext):
    global listUniv
    id = listUniv[message.text]
    univ = message.text
    await get_description(message,id)
    await state.update_data(univ=univ)
    await state.update_data(id=id)
    await state.reset_state(with_data=False)


@dp.callback_query_handler(text="application")
async def application(call: types.CallbackQuery,state: FSMContext):

    data = await state.get_data()
    id = data.get('id')
    email = data.get('user_email')
    id_tg = await get_id_tg(id)
    univ = data.get('univ')

    await bot.send_message(ADMINS, f"Пользователь {email} хочет поступить в ваше заведение {univ}")
    await bot.send_message(call.message.chat.id, f"Заявка отправлина ожидайте ответа!!!")

    await menu(message=call.message, state=state)



async def get_unev(keyboard, listUniv, txt):
    url = 'https://api.sokratapp.ru/study_partners/'

    r = requests.get(url=url)

    r_unew = r.json()

    res = r_unew["results"]
    for re in res :
        if re["partner_type"] == "VUZ":
            button1 = types.KeyboardButton(text=re['name'])
            id = re["id"]
            listUniv[re['name']] = id
            txt += f'{re["name"]},\n'
            keyboard.row(button1)
    return txt


async def get_id_tg(id):
    url = f'https://api.sokratapp.ru/study_partners/{id}'

    r = requests.get(url=url)

    r = r.json()

    return r['telegram_id']


async def get_description(message: types.Message, id):
    url = f'https://api.sokratapp.ru/study_partners/{id}'

    r = requests.get(url=url)

    r = r.json()

    description = r["description"]

    if r['image'] != None:
        photo = r['image']
    else:
        photo = 'https://t-bike.ru/images/products/no-image.jpg'
    keyboard = types.InlineKeyboardMarkup()

    button1 = types.InlineKeyboardButton(text="Отправить заявку", callback_data="application")
    button2 = types.InlineKeyboardButton(text="В личный кабинет", callback_data="menu")

    keyboard.row(button1)
    keyboard.row(button2)


    await bot.send_photo(chat_id=message.chat.id,
                         photo=photo,
                         caption=description,
                         reply_markup=keyboard)

    await bot.send_message(chat_id=message.chat.id,
                           text="Ожидаем вашего ответа!!",
                           reply_markup=types.ReplyKeyboardRemove())