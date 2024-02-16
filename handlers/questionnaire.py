from aiogram import types, Dispatcher
from config import bot
from keyboards import questionnaire_inline_buttons


async def questionnaire_start(call: types.callback_query):
    await bot.send_message(
        chat_id=call.from_user.id,
        text="Latte 🥛 or Americano ☕ ?",
        reply_markup=await questionnaire_inline_buttons.questionnaire_keyboard()
    )


async def latte_answer(call: types.callback_query):
    await call.message.delete()
    await bot.send_message(
        chat_id=call.from_user.id,
        text="That's nice, I love when a lot of milk as well\n"
             "Do you prefer it when more sugar or less?",
        reply_markup=await questionnaire_inline_buttons.latte_questionnaire_keyboard()
    )


async def americano_answer(call: types.callback_query):
    await call.message.delete()
    await bot.send_message(
        chat_id=call.from_user.id,
        text="Americano is very strong, I like that",
    )


async def more_sugar_answer(call: types.callback_query):
    await call.message.delete()
    await bot.send_message(
        chat_id=call.from_user.id,
        text="Be careful with the amount of sugar it's may be unhealthy"
    )


async def less_sugar_answer(call: types.callback_query):
    await call.message.delete()
    await bot.send_message(
        chat_id=call.from_user.id,
        text="It's cool but the taste is a little bland"
    )


def register_questionnaire_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(
        questionnaire_start,
        lambda call: call.data == "start_questionnaire"
    )
    dp.register_callback_query_handler(
        latte_answer,
        lambda call: call.data == "latte"
    )
    dp.register_callback_query_handler(
        americano_answer,
        lambda call: call.data == "americano"
    )
    dp.register_callback_query_handler(
        more_sugar_answer,
        lambda call: call.data == "more sugar"
    )
    dp.register_callback_query_handler(
        less_sugar_answer,
        lambda call: call.data == "less sugar"
    )
