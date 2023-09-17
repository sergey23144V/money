import requests
from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import ADMINS
from handlers.users.mechanic import menu, money_for_grades, mesAdmin, GetToken
from loader import dp, bot
from states.ClassUser import User


@dp.callback_query_handler(text="setting")
async def settings(call: types.CallbackQuery,state: FSMContext):
    keyboard = types.InlineKeyboardMarkup()



    data = await state.get_data()

    user_name = data.get('user_name')
    if  user_name == None or user_name == '  ':
        button2 = types.InlineKeyboardButton(text="Ваше ФИО (+🟡1000)", callback_data="name")
    else:
        button2 = types.InlineKeyboardButton(text="Изменить имя", callback_data="name")
    keyboard.row(button2)

    user_city = data.get('user_city')
    if user_city == None:
        button3 = types.InlineKeyboardButton(text="Ваш город (+🟡1000)", callback_data="city")
        keyboard.row(button3)

    user_school = data.get('user_school')
    if user_school == None:
        button4 = types.InlineKeyboardButton(text="Номер школы (+🟡1000)", callback_data="school")
        keyboard.row(button4)

    user_class = data.get('user_class')
    if user_class == None:
        button5 = types.InlineKeyboardButton(text="Ваш класс (+🟡1000)", callback_data="class")
        keyboard.row(button5)

    user_choice = data.get('user_choice')
    if user_choice == None:
        button6 = types.InlineKeyboardButton(text="Куда хотите поступить (+🟡2000)", callback_data="choice")
        keyboard.row(button6)

    phon = data.get('user_phon')
    if phon == '':
        button7 = types.InlineKeyboardButton(text="Ваш телефона (+🟡2000)", callback_data="phon")
        keyboard.row(button7)

    button1 = types.InlineKeyboardButton(text="Вернуться в кабинет", callback_data="menu")
    keyboard.row(button1)
    await bot.send_photo(chat_id=call.message.chat.id,
                         photo="https://downloader.disk.yandex.ru/preview/be8c6828c1e6e75e96a8e49a43cf77659ca674e43184fc052444abf34d61d53a/642c66a8/ZA5nVuIWol8rtRW1_HfPdkr9N2DqxgbnVTwuaGpxRfbqKB8X4Rv4XveNYgEnFi37mZoWyINjeUnDjXMa-zJdHw%3D%3D?uid=0&filename=Картинка%205%20–%202.png&disposition=inline&hash=&limit=0&content_type=image%2Fpng&owner_uid=0&tknv=v2&size=1855x947",
                         caption='Здесь ты можешь настроить свой профиль', reply_markup=keyboard)

    data = await state.get_data()
    email = data.get('user_email')
    await mesAdmin( f"Пользователь {email} перешел в настройки", state)


@dp.callback_query_handler(text="city")
async def city(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer('Введите свой город:')
    await User.user_city.set()


@dp.message_handler(state=User.user_city)
async def user_city(message: types.Message, state: FSMContext):
        text = message.text
        await state.update_data(user_city=text)
        await state.reset_state(with_data=False)
        await money_for_grades(1000, state=state)
        data = await state.get_data()
        email = data.get('user_email')
        await mesAdmin(f"Пользователь {email} заполнил Город (+🟡1000)", state)
        await menu(message, state)


@dp.callback_query_handler(text="name")
async def name_user(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer('Введите вашу фамилию:')
    data = await state.get_data()

    user_name = data.get('user_name')
    if user_name == None or user_name == '  ':
        await money_for_grades(1000, state=state)

    await User.user_last_name.set()


@dp.message_handler(state=User.user_last_name)
async def name_user(message: types.Message, state: FSMContext):
        text = message.text
        await state.update_data(user_last_name=text)
        await state.reset_state(with_data=False)
        await message.answer('Введите вашe имя:')
        await User.user_name.set()


@dp.message_handler(state=User.user_name)
async def name_user(message: types.Message, state: FSMContext):
        text = message.text
        await state.update_data(user_name=text)
        await state.reset_state(with_data=False)
        await message.answer('Введите вашe отчество:')
        await User.user_middle_name.set()


@dp.message_handler(state=User.user_middle_name)
async def name_user(message: types.Message, state: FSMContext):
        text = message.text
        await state.update_data(user_middle_name=text)
        await state.reset_state(with_data=False)


        url_user = f"https://api.sokratapp.ru/api/user_me"

        data = await state.get_data()
        user_token = await GetToken(state)
        last_name = data.get('user_last_name')
        first_name = data.get('user_name')
        middle_name = data.get('user_middle_name')

        headers = {'Authorization': f'Token {user_token}'}

        grades = {'last_name': f'{last_name}',
                  'first_name': f'{first_name}',
                  'middle_name': f'{middle_name}'
                  }

        requests.patch(url=url_user, headers=headers, data=grades)

        name = last_name + " " + first_name + " " + middle_name
        await state.update_data(user_name=name)
        data = await state.get_data()
        email = data.get('user_email')
        await mesAdmin( f"Пользователь {email} заполнил ФИО (+🟡1000)",state)

        await menu(message, state)

async def api_citi(citi, state: FSMContext):
    url_user = f"https://api.sokratapp.ru/api/user_me"

    data = await state.get_data()
    user_token = data.get('token')

    headers = {'Authorization': f'Token {user_token}'}

    grades = {'city': f'{citi}'}

    requests.patch(url=url_user, headers=headers, data=grades)


@dp.callback_query_handler(text="school")
async def school(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer('Введите свою школу:')
    await User.user_school.set()


@dp.message_handler(state=User.user_school)
async def user_school(message: types.Message, state: FSMContext):
    text = message.text
    await state.update_data(user_school=text)
    await state.reset_state(with_data=False)
    await money_for_grades(1000, state=state)
    data = await state.get_data()
    email = data.get('user_email')
    await mesAdmin(f"Пользователь {email} заполнил школу (+🟡1000)", state)
    await menu(message, state)


@dp.callback_query_handler(text="class")
async def _class(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer('Введите свой класс:')
    await User.user_class.set()


@dp.message_handler(state=User.user_class)
async def user_class(message: types.Message, state: FSMContext):
    text = message.text
    await state.update_data(user_class=text)
    await state.reset_state(with_data=False)
    await money_for_grades(1000, state=state)

    data = await state.get_data()
    email = data.get('user_email')
    await mesAdmin( f"Пользователь {email} заполнил класс (+🟡1000)", state)
    await menu(message, state)


@dp.callback_query_handler(text="choice")
async def _choice(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer('Введите куда хотите поступить:')
    await User.user_choice.set()


@dp.message_handler(state=User.user_choice)
async def user_choice(message: types.Message, state: FSMContext):
    text = message.text
    await state.update_data(user_choice=text)
    await state.reset_state(with_data=False)
    await money_for_grades(2000, state=state)

    data = await state.get_data()
    email = data.get('user_email')
    await mesAdmin( f"Пользователь {email} заполнил желаемого завидения  (+🟡2000)", state)
    await menu(message, state)


@dp.callback_query_handler(text="phon")
async def _choice(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer('Введите свой номер телефона:')
    await User.user_phon.set()


@dp.message_handler(state=User.user_phon)
async def user_choice(message: types.Message, state: FSMContext):
    text = message.text
    url_user = f"https://api.sokratapp.ru/api/user_me"

    data = await state.get_data()
    user_token = await GetToken(state)

    headers = {'Authorization': f'Token {user_token}'}

    grades = {'phone': f'{text}'}

    r_phon = requests.patch(url=url_user, headers=headers, data=grades)



    if (r_phon.status_code != 400):
        await state.update_data(user_phon=text)
        await state.reset_state(with_data=False)
        await money_for_grades(2000, state=state)
        email = data.get('user_email')
        await mesAdmin( f"Пользователь {email} заполнил телефон  (+🟡2000)", state)
        await menu(message, state)
    else:
        await message.answer('Неправильно введен номер!\nВведите его повторно')
        await state.reset_state(with_data=False)
        await User.user_phon.set()

