from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)


async def questionnaire_keyboard():
    markup = InlineKeyboardMarkup()
    latte_button = InlineKeyboardButton(
        "Latte 🥛",
        callback_data="latte"
    )
    americano_button = InlineKeyboardButton(
        "Americano ☕",
        callback_data="americano"
    )
    markup.add(latte_button)
    markup.add(americano_button)
    return markup


async def latte_questionnaire_keyboard():
    markup = InlineKeyboardMarkup()
    more_sugar_button = InlineKeyboardButton(
        "More",
        callback_data="more sugar"
    )
    less_sugar_button = InlineKeyboardButton(
        "Less",
        callback_data="less sugar"
    )
    markup.add(more_sugar_button)
    markup.add(less_sugar_button)
    return markup
