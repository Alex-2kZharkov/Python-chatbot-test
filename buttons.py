from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


categories_buttons_count = 0


def setButtonsCount(number: int):
    global categories_buttons_count
    categories_buttons_count = number


action_callback = CallbackData("action", "action_type")


button_start = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Начать тест⚡️", callback_data="action:start")]
    ]
)


categories_buttons = InlineKeyboardMarkup()


def set_categories_buttons_count(ids):
    i = 0
    for x in range(categories_buttons_count):
        categories_buttons.add(InlineKeyboardButton(text=f"Тест №{i+1}", callback_data=f"action:btn{ids[i]}"))
        i += 1


button_pick_options = InlineKeyboardMarkup(row_width=2)


def set_button_pick_options():
    button_start_test = InlineKeyboardButton(text="Перейти к тесту", callback_data="action:start_test")
    button_cancel_test = InlineKeyboardButton(text="Отмена", callback_data="action:cancel_test")
    button_pick_options.insert(button_cancel_test)
    button_pick_options.insert(button_start_test)

