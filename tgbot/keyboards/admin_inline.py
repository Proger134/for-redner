from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

apply_mailing_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Yes", callback_data="mailing:yes"),
            InlineKeyboardButton(text="No", callback_data="mailing:no")
        ]
    ]
)
