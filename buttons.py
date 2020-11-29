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
    print("!!!!")
    print(categories_buttons_count)
    for x in range(categories_buttons_count):
        print(x)
        categories_buttons.add(InlineKeyboardButton(text=f"Тест №{i+1}", callback_data=f"action:{ids[i]}"))
        i += 1