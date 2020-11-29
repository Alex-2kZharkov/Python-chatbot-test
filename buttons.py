from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


categories_buttons_count = 0
current_buttons_number = 0
is_options_buttons_shown = False
categories_buttons = InlineKeyboardMarkup()
button_pick_options = InlineKeyboardMarkup(row_width=2)

def setButtonsCount(number: int):
    global categories_buttons_count, current_buttons_number
    categories_buttons_count = number
    current_buttons_number += number


action_callback = CallbackData("action", "action_type")


button_start = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Начать тест⚡️", callback_data="action:start")]
    ]
)




def set_categories_buttons_count(ids):
    global categories_buttons_count, current_buttons_number
    if current_buttons_number > categories_buttons_count:
        current_buttons_number -= categories_buttons_count
    else:
        i = 0
        for x in range(categories_buttons_count):
            categories_buttons.add(InlineKeyboardButton(text=f"Тест №{i + 1}", callback_data=f"action:btn{ids[i]}"))
            i += 1


def set_button_pick_options():
    global is_options_buttons_shown

    if not is_options_buttons_shown:

        button_start_test = InlineKeyboardButton(text="Перейти к тесту 👉", callback_data="action:start_test")
        button_cancel_test = InlineKeyboardButton(text="Вернуться к выбору теста 👈", callback_data="action:change_test")

        button_pick_options.insert(button_cancel_test)
        button_pick_options.insert(button_start_test)
        is_options_buttons_shown = True



