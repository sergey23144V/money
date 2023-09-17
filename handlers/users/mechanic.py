

from aiogram import types
from aiogram.dispatcher import FSMContext
import requests
from datetime import datetime
from data.config import ADMINS
from handlers.users.instruction import instruction
from handlers.users.start import count_user

from loader import dp, bot
from states.ClassUser import User


@dp.callback_query_handler(text="connect_program",state=User.user_email)
async def connect(call: types.CallbackQuery, state: FSMContext):
    await _connect(call.message)


async def _connect(message: types.Message):
    await message.answer("Введите вашу почту, для начала авторизации.")
    await User.user_email.set()


@dp.message_handler(state=User.user_email)
async def password(message: types.Message, state: FSMContext):
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text="Изменить почту", callback_data="connect_program")
    button2 = types.InlineKeyboardButton(text="Продолжить", callback_data="Next")

    keyboard.row(button1)
    keyboard.row(button2)
    async with state.proxy() as data:
        data['email'] = message.text
        if await checkEmail(message.text):
            await message.answer("Ваш профиль найден!", reply_markup=keyboard)
            data['new_user'] = False
        else:
            button2.text = "Регистрация"
            await message.answer("Ваш профиль не найден.\nПройдите регестрацию пожалуйста", reply_markup=keyboard)
            data['new_user'] = True


@dp.callback_query_handler(text="Next", state=User.user_email)
async def registr_1(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Введите пароль для подтверждения:")
    await User.user_password.set()


@dp.message_handler(state=User.user_password)
async def password(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        new_user = data['new_user']
        if (new_user):
            await message.answer("Введите пароль потворно")
            data["user_password"] = message.text
            await User.user_password_sweaty.set()
        else:
            await Authorization(message, state)


@dp.message_handler(state=User.user_password_sweaty)
async def Registration(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        email = data['email']
        password_user = data["user_password"]
        await state.finish()
        await user_reg(email, password_user, message, state)


async def Authorization(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        password_user = message.text
        data["user_password"] = password_user
        await state.update_data(user_password=password_user)
        email = data['email']
        await authorizeUser(email, password_user, message, state)


async def authorizeUser(mail, password_user, message: types.Message, state: FSMContext):
    url = "https://api.sokratapp.ru/api/api-token-auth/"
    data_auto = {
        "username": f"{mail}",
        "password": f"{password_user}"
    }
    try:
        r_admin = requests.post(url, data=data_auto)
        r_admin_json = r_admin.json()

        user_token = r_admin_json["token"]
        await state.update_data(token=user_token)
        await menu(message,state)
        await state.reset_state(with_data=False)
    except:
        await message.answer("Неверный пароль или логин")
        await message.answer("Введите пароль потворно")


async def checkEmail(email):
    url = 'https://api.sokratapp.ru/api/users/check_email/'

    data = {

        "email": email
    }

    r = requests.get(url=url, data=data)

    try:
        r.raise_for_status()
        return True
    except:
        return False


async def menu(message: types.Message, state: FSMContext):
    await GetUserData(state)
    keyboard = types.InlineKeyboardMarkup()

    button2 = types.InlineKeyboardButton(text="Онлайн поступление", callback_data="entrance")
    button3 = types.InlineKeyboardButton(text="Получить монеты", callback_data="exchange")
    button4 = types.InlineKeyboardButton(text="Школьный магазин", callback_data="shop")
    button5 = types.InlineKeyboardButton(text="Подбери репититора",
                                         url="https://api.sokratapp.ru/api/courses/category/repetitori/")
    button6 = types.InlineKeyboardButton(text="Настройки", callback_data="setting")

    keyboard.row(button3)
    keyboard.row(button2)
    keyboard.row(button4)
    keyboard.row(button5)
    keyboard.row(button6)

    data = await state.get_data()

    email = data.get('user_email')

    name = data.get('user_name')

    if name == None or name == '  ':
        name = '--------------------------------------'

    phon = data.get('user_phon')
    if phon == None or phon == '':
        phon = '--------'

    score_user = data.get('user_score')
    if score_user == None or score_user == 0:
        await money_for_grades(1000, state=state)
        score_user = 1000

    user_city = data.get('user_city')
    if user_city == None:
        user_city = '--------'
    user_school = data.get('user_school')
    if user_school == None:
        user_school = '--------'
    user_class = data.get('user_class')
    if user_class == None:
        user_class = '--------'
    user_choice = data.get('user_choice')
    if user_choice == None:
        user_choice = '--------'

    await bot.send_photo(chat_id=message.chat.id,
                         photo="https://downloader.disk.yandex.ru/preview/269dea1c26fd03511dc15c8f882192d1cb426565d3ebab81ca395fe36ad19a34/64349bd6/Eb7aDNN3SyZbfZoHBZKdVEr9N2DqxgbnVTwuaGpxRfavoL5Ma0_a80ZJBMrut8AitqUo7oGWHMZa1xwj9fou9Q%3D%3D?uid=0&filename=Картинка%205.png&disposition=inline&hash=&limit=0&content_type=image%2Fpng&owner_uid=0&tknv=v2&size=714x943",
                         caption=f"👤 Ваш профиль:\n                    ФИО\n{name}\nВаша почта: {email}  \nВаш телефон:  {phon}\n"
                                 f"Город: {user_city} \nНомер школы: {user_school}\nКласс: {user_class}\nКуда планируете поступать: {user_choice}\n"
                                 f"\nВаши монеты Сократа: 🟡{score_user}"
                                 f"\n\n↪️ Пригласи друга: https://t.me/Kalinenocbot",
                         reply_markup=keyboard)

    await mesAdmin("Перешел в личный кабинет", state)


async def mesAdmin(text, state: FSMContext):
    data = await state.get_data()
    email = data.get('email')
    for admin in ADMINS:
        await bot.send_message(admin, f"Пользователь {email} {text}")


async def mesAdminScope(message: types.Message, state: FSMContext, photo, score):
    data = await state.get_data()
    now = datetime.now()
    email = data.get('email')
    for admin in ADMINS:
        await bot.send_photo(chat_id=admin,
                         photo=photo,
                         caption=f'{message.from_user.id}\nНовая оценка пользователя @{message.from_user.username}\n{email}\n{now.strftime("%d-%m-%Y %H:%M")}\nОценка: {score}\n')


async def user_reg(email, password_user, message: types.Message, state: FSMContext):
    if message.text == password_user:
        url = 'https://api.sokratapp.ru/api/users/signup/'

        body = {
            "email": f"{email}",
            "password": f'{password_user}'
        }

        r = requests.post(url=url, data=body)

        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="Выполнить авторизацию", callback_data="connect_program"))

        await message.answer("Успешно", reply_markup=keyboard)
        await count_user()
    else:
        await message.answer("Введены не соответствующие пароли")
        await message.answer("Введите пароль потворно")
        await state.reset_state(with_data=False)
        await User.user_password_sweaty.set()


async def money_for_grades(count, state: FSMContext):
    url_user = f"https://api.sokratapp.ru/api/user_me"

    user_token = await GetToken(state)

    headers = {'Authorization': f'Token {user_token}'}

    r_user = requests.get(url=url_user, headers=headers)
    r_user_json = r_user.json()

    score_user = r_user_json['money_for_grades'] + count

    await state.update_data(user_score=score_user)

    grades = {'money_for_grades': f'{score_user}'}
    r = requests.patch(url=url_user, headers=headers, data=grades)


async def GetToken(state: FSMContext):
    data = await state.get_data()

    mail =  data.get('email')
    password_user = data.get("user_password")
    url = "https://api.sokratapp.ru/api/api-token-auth/"
    data_auto = {
        "username": f"{mail}",
        "password": f"{password_user}"
    }
    r_admin = requests.post(url, data=data_auto)
    r_admin_json = r_admin.json()

    user_token = r_admin_json["token"]
    return user_token

async def GetUserData(state: FSMContext):
    token = await GetToken(state)
    url_user = f"https://api.sokratapp.ru/api/user_me"
    headers = {'Authorization': f'Token {token}'}

    r_user = requests.get(url=url_user, headers=headers)

    r_user_json = r_user.json()

    name = r_user_json['last_name'] + " " + r_user_json['first_name'] + " " + r_user_json['middle_name']

    await state.update_data(user_name=name)

    email = r_user_json['email']
    await state.update_data(user_email=email)

    score_user = r_user_json['money_for_grades']
    await state.update_data(user_score=score_user)

    phon = r_user_json['phone']
    await state.update_data(user_phon=phon)

