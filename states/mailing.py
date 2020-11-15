from aiogram.dispatcher.filters.state import State, StatesGroup


class Mailing(StatesGroup):
    Buttons = State()
    PreMail = State()
    Confirm = State()


class ToSub(StatesGroup):
    Add_Input = State()
    Add_Commit = State()
    Add_By_self = State()
    Delete = State()


class Wait(StatesGroup):
    Wait = State()
