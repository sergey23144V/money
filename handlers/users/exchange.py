from aiogram import types
from aiogram.dispatcher import FSMContext

from aiogram.types import ContentType

from datetime import datetime
from data.config import ADMINS

from handlers.users.mechanic import money_for_grades, menu

from loader import dp, bot
from states.ClassUser import User

score = 0


@dp.callback_query_handler(text="exchange")
async def exchange(call: types.CallbackQuery, state: FSMContext):
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text="Обменять сейчас", callback_data="score")
    button2 = types.InlineKeyboardButton(text="Вернуться в кабинет", callback_data="menu")


    keyboard.row(button1)
    keyboard.row(button2)
    await bot.send_photo(chat_id=call.message.chat.id,
                         photo="https://downloader.disk.yandex.ru/preview/be8c6828c1e6e75e96a8e49a43cf77659ca674e43184fc052444abf34d61d53a/642c66a8/ZA5nVuIWol8rtRW1_HfPdkr9N2DqxgbnVTwuaGpxRfbqKB8X4Rv4XveNYgEnFi37mZoWyINjeUnDjXMa-zJdHw%3D%3D?uid=0&filename=Картинка%205%20–%202.png&disposition=inline&hash=&limit=0&content_type=image%2Fpng&owner_uid=0&tknv=v2&size=1855x947",
                         caption='Старина Сократ готов обменять "пару монет" на твои оценки! Нажми "обменять сейчас" и '
                                 'следуй подсказкам бота!', reply_markup=keyboard)
    data = await state.get_data()
    email = data.get('user_email')


@dp.callback_query_handler(text="score")
async def score(call: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    button6 = types.InlineKeyboardButton(text="Оценка1️⃣", callback_data="score1")
    button1 = types.InlineKeyboardButton(text="Оценка2️⃣", callback_data="score2")
    button2 = types.InlineKeyboardButton(text="Оценка3️⃣", callback_data="score3")
    button3 = types.InlineKeyboardButton(text="Оценка4️⃣", callback_data="score4")
    button4 = types.InlineKeyboardButton(text="Оценка5️⃣", callback_data="score5")
    button5 = types.InlineKeyboardButton(text="Вернуться в кабинет", callback_data="menu")

    keyboard.row(button6)
    keyboard.row(button1)
    keyboard.row(button2)
    keyboard.row(button3)
    keyboard.row(button4)
    keyboard.row(button5)
    await bot.send_photo(chat_id=call.message.chat.id,
                         photo="https://downloader.disk.yandex.ru/preview/a7f4f13ea8fe7f89e0595f776418abbdf1fdbb1283540f8192a5afcfb5570aa3/642cafff/iTNkI8EULZ8fmwYpDw0y3_zTC4RilJy5MysE2VhIeo3-yNkC2lTvSaghHn0xE4OoA-DOZPsMF6H5WeSixGDGeg%3D%3D?uid=0&filename=Картинка%205%20–%204.png&disposition=inline&hash=&limit=0&content_type=image%2Fpng&owner_uid=0&tknv=v2&size=1855x947",
                         caption='Сейчас выбери оценку какую хочешь обменять!', reply_markup=keyboard)


@dp.callback_query_handler(text="score1")
async def score1(call: types.CallbackQuery, state: FSMContext):
    global score
    score = 1

    await mes(call)
    await money_for_grades(500, state=state)
    await User.photo.set()


@dp.callback_query_handler(text="score2")
async def score2(call: types.CallbackQuery, state: FSMContext):
    global score
    score = 2

    await mes(call)
    await money_for_grades(750, state=state)
    await User.photo.set()


@dp.callback_query_handler(text="score3")
async def score3(call: types.CallbackQuery, state: FSMContext):
    global score
    score = 3

    await mes(call)
    await money_for_grades(1000, state=state)
    await User.photo.set()


@dp.callback_query_handler(text="score4")
async def score4(call: types.CallbackQuery, state: FSMContext):
    global score
    score = 4

    await mes(call)
    await money_for_grades(1250, state=state)
    await User.photo.set()


@dp.callback_query_handler(text="score5")
async def score5(call: types.CallbackQuery, state: FSMContext):
    global score
    score = 5

    await mes(call)
    await money_for_grades(1500, state=state)
    await User.photo.set()


@dp.message_handler(state=User.photo, content_types=ContentType.PHOTO)
async def photo(message: types.Message, state: FSMContext):
        global score
        now = datetime.now()
        photo = message.photo[-1].file_id

        data = await state.get_data()
        score_user = data.get('user_score')
        email = data.get('user_email')

        await state.update_data(photo=photo)
        await bot.send_photo(chat_id=ADMINS,
                             photo=photo,
                             caption=f'{message.from_user.id}\nНовая оценка пользователя @{message.from_user.username}\n{email}\n{now.strftime("%d-%m-%Y %H:%M")}\nОценка: {score}\n')
        await bot.send_message(chat_id=message.chat.id,text=
                             f'@{message.from_user.username}, это фантастика! Твой кошелек пополнен! \nТвой баланс {score_user} монеты Сократа! '
                                     'Повтори процедуру, чтобы обменять еще оценки! ')
        await state.reset_state(with_data=False)
        await menu(message, state=state)


async def mes(call: types.CallbackQuery):
    await bot.send_photo(chat_id=call.message.chat.id,
                         photo="https://downloader.disk.yandex.ru/preview/fd35908e0d6991061c23a7c534b46173fcc90aa411de7c95420f7ddd4cf842d5/642d780e/cILctKHHTPpye9hZrfk2pswn9UAddKPyuOYFeW-Vq3ZD-eXuvJUcf2L9yPhNEWVjgKkT3dr0qO3YhAnCsHJwPA%3D%3D?uid=0&filename=Картинка%205%20–%205.png&disposition=inline&hash=&limit=0&content_type=image%2Fpng&owner_uid=0&tknv=v2&size=1855x947",
                         caption='Вы на верном пути! Осталось подтвердить свою оценку. Отправь фото из дневника.\n'
                                 '1) Нажмите на "Скрепку";\n'
                                 '2) Сделайте фото оценки или выберите ее из галереи;\n'
                                 '3) Отправьте ее боту;\n'
                                 '4) На фото должны быть видны: дата и день недели и оценка з аэтот день.\n'
                                 '5) Если у вас несколько оценок в один день, обменяйте столько оценок, сколько их у вас в этот день.\n'
                                 '_______________________________\n'
                                 'Внимание! Мы проверяем все фото. Если фото не соответствует правилам сервиса, начисление за эту оценку будет аннулировано.',
                         )



