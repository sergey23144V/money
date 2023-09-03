from aiogram import types

from loader import dp, bot



@dp.callback_query_handler(text="acquaintance1")
async def acquaintance1(call: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Далее 1 из 4", callback_data="acquaintance2"))
    await bot.send_photo(chat_id=call.message.chat.id,
                         photo="https://downloader.disk.yandex.ru/preview/708da2a1ba2954484472febd4d67d676fff3265c67cc33b7763359a40c54d7b7/641b2f71/aav889LViY80SFUJZROaEjgDvA_RgSmArNa4MWmSMaCDjBzheks2RgabpYMt1IWnDWFHGuiykGvN0iSzLZcCaQ%3D%3D?uid=0&filename=Картинка%201.png&disposition=inline&hash=&limit=0&content_type=image%2Fpng&owner_uid=0&tknv=v2&size=1855x947",
                         reply_markup=keyboard)

@dp.callback_query_handler(text="acquaintance2")
async def acquaintance1(call: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Далее 2 из 4", callback_data="acquaintance3"))
    await bot.send_photo(chat_id=call.message.chat.id,
                         photo='https://downloader.disk.yandex.ru/preview/f1bf14609fe9ab49f60e1018eeb84baca46650cd752b952d32bdaf1ec7b6c41f/643c2ad5/LE9bacKsz44tCCp5izQUPxJ8-319z0ErntJgnFLZibaYwhNK3KGqRtNihID-r5tRq4uRFUf9zs2tW40lhHRjSg%3D%3D?uid=0&filename=шаг%202.png&disposition=inline&hash=&limit=0&content_type=image%2Fpng&owner_uid=0&tknv=v2&size=893x943',
                         reply_markup=keyboard)

@dp.callback_query_handler(text="acquaintance3")
async def acquaintance1(call: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Далее 3 из 4", callback_data="acquaintance4"))
    await bot.send_photo(chat_id=call.message.chat.id,
                         photo='https://downloader.disk.yandex.ru/preview/14b74af0b2bc99fafc7ab177e40a35354d92572727e496344699f86996f579fd/643c2ad5/c0vD2HsS8bgxybwgRs7_nBJ8-319z0ErntJgnFLZibb2FMMTqoBHkh3XiaopN4S0AgG3XP7zToSrJOyFBtv-7w%3D%3D?uid=0&filename=шаг%203.png&disposition=inline&hash=&limit=0&content_type=image%2Fpng&owner_uid=0&tknv=v2&size=893x943'
                        ,reply_markup=keyboard)

@dp.callback_query_handler(text="acquaintance4")
async def acquaintance3(call: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Получить первые 1000 монет", callback_data="connect_program"))
    await bot.send_photo(chat_id=call.message.chat.id,
                         photo="https://downloader.disk.yandex.ru/preview/e9599f3bb92d46099f03878960e455d8f839b24b3201b7e08faaa04aab2247e0/641b2f71/UHyX3SC38i03tcHZeugg2zgDvA_RgSmArNa4MWmSMaAju5NW2rzj6hCzx5XNaPzYjzPrupLrYk3rMo_85KYgkQ%3D%3D?uid=0&filename=Картинка%204.png&disposition=inline&hash=&limit=0&content_type=image%2Fpng&owner_uid=0&tknv=v2&size=1855x947",
                         reply_markup=keyboard)
