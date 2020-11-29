from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

action_callback = CallbackData("action", "action_type")


button_start = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Начать тест⚡️", callback_data="action:start")]
    ]
)
