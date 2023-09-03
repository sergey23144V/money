from aiogram.dispatcher.filters.state import State, StatesGroup



class User(StatesGroup):
    user_name = State()
    user_last_name = State()
    user_middle_name = State()
    user_email = State()
    user_phon = State()
    user_password = State()
    user_password_sweaty = State()
    user_score = State()
    user_city = State()
    user_school = State()
    user_class = State()
    user_choice = State()
    photo = State()
    token = State()
    new_user = State()
    univ = State()
    id = State()