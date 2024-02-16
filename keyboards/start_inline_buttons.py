from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)


async def start_keyboard():
    markup = InlineKeyboardMarkup()
    questionnaire_button = InlineKeyboardButton(
        "Questionnaire 📄",
        callback_data="start_questionnaire"
    )
    markup.add(questionnaire_button)
    return markup
