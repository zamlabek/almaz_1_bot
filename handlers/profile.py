import sqlite3

from aiogram import types, Dispatcher

import const
from config import bot
from database.bot_db import Database
from keyboards.profile_inline_buttons import (
    my_profile_keyboard,
    like_dislike_keyboard,
)
import random
import re


async def my_profile_call(call: types.CallbackQuery):
    db = Database()
    profile = db.sql_select_profile(
        tg_id=call.from_user.id
    )

    if profile:
        with open(profile['photo'], 'rb') as photo:
            await bot.send_photo(
                chat_id=call.from_user.id,
                photo=photo,
                caption=const.PROFILE_TEXT.format(
                    nickname=profile['nickname'],
                    first_name=profile['first_name'],
                    last_name=profile['last_name'],
                    bio=profile['bio'],
                    age=profile['age'],
                    zodiac_sign=profile['zodiac_sign'],
                ),
                reply_markup=await my_profile_keyboard()
            )
    else:
        await bot.send_message(
            chat_id=call.from_user.id,
            text='U did not registered yet\n'
                 'Please register to view ur profile'
        )


async def random_filter_profile_call(call: types.CallbackQuery):
    if call.message.caption.startswith("Nickname"):
        await call.message.delete()
    db = Database()
    profiles = db.sql_select_all_profiles(
        tg_id=call.from_user.id
    )
    print(profiles)
    if not profiles:
        await bot.send_message(
            chat_id=call.from_user.id,
            text='You have liked all profiles!'
        )
        return

    random_profile = random.choice(profiles)
    with open(random_profile['photo'], 'rb') as photo:
        await bot.send_photo(
            chat_id=call.from_user.id,
            photo=photo,
            caption=const.PROFILE_TEXT.format(
                nickname=random_profile['nickname'],
                first_name=random_profile['first_name'],
                last_name=random_profile['last_name'],
                bio=random_profile['bio'],
                age=random_profile['age'],
                zodiac_sign=random_profile['zodiac_sign'],
            ),
            reply_markup=await like_dislike_keyboard(
                tg_id=random_profile['telegram_id']
            )
        )


async def detect_like_call(call: types.CallbackQuery):
    owner = re.sub("like_", "", call.data)
    print(owner)
    db = Database()
    try:
        db.sql_insert_like(
            owner=owner,
            liker=call.from_user.id
        )
    except sqlite3.IntegrityError:
        await bot.send_message(
            chat_id=call.from_user.id,
            text='You have liked this profile!'
        )
        return
    finally:
        await call.message.delete()
        await random_filter_profile_call(call=call)


def register_profile_handler(dp: Dispatcher):
    dp.register_callback_query_handler(
        my_profile_call,
        lambda call: call.data == 'my_profile'
    )
    dp.register_callback_query_handler(
        random_filter_profile_call,
        lambda call: call.data == 'random_profiles'
    )
    dp.register_callback_query_handler(
        detect_like_call,
        lambda call: 'like_' in call.data
    )
