from aiogram.fsm.state import State, StatesGroup


class BuySO2Gold(StatesGroup):
    amount = State()


class BuyTGStars(StatesGroup):
    target = State()
    username = State()
    amount = State()


class AdminAddProduct(StatesGroup):
    name = State()
    desc = State()
    price = State()
    login = State()
    password = State()
    photo = State()
