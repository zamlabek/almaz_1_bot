from aiogram import types, Dispatcher
from config import bot, MEDIA_DESTINATION
from database import bot_db
from keyboards import start_inline_buttons
import const
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class RegistrationStates(StatesGroup):
    nickname = State()
    first_name = State()
    last_name = State()
    biography = State()
    age = State()
    zodiac_sign = State()
    photo = State()


async def registration_start(call: types.CallbackQuery):
    await bot.send_message(
        chat_id=call.from_user.id,
        text='Send me your nickname please! 🥷'
    )
    await RegistrationStates.nickname.set()


async def load_nickname(message: types.Message,
                        state: FSMContext):
    async with state.proxy() as data:
        data['nickname'] = message.text

    await bot.send_message(
        chat_id=message.from_user.id,
        text='Send me your first name! ✅'
    )
    await RegistrationStates.next()


async def load_first_name(message: types.Message,
                          state: FSMContext):
    async with state.proxy() as data:
        data['first_name'] = message.text

    await bot.send_message(
        chat_id=message.from_user.id,
        text='Send me your last name! ✅'
    )
    await RegistrationStates.next()


async def load_last_name(message: types.Message,
                         state: FSMContext):
    async with state.proxy() as data:
        data['last_name'] = message.text

    await bot.send_message(
        chat_id=message.from_user.id,
        text='Send me your biography! 🗿'
    )
    await RegistrationStates.next()


async def load_bio(message: types.Message,
                   state: FSMContext):
    async with state.proxy() as data:
        data['bio'] = message.text

    await bot.send_message(
        chat_id=message.from_user.id,
        text='How old are you? 🪪\n'
             '(Send me only numeric text)'
    )
    await RegistrationStates.next()


async def load_age(message: types.Message,
                   state: FSMContext):
    try:
        int(message.text)
    except ValueError:
        await bot.send_message(
            chat_id=message.from_user.id,
            text="I told you send only numeric text\n"
                 "registration failed❌\n"
                 "Restart registration!"
        )
        await state.finish()
        return

    async with state.proxy() as data:
        data['age'] = int(message.text)

    await bot.send_message(
        chat_id=message.from_user.id,
        text='Send me your zodiac sign 🌙'
    )
    await RegistrationStates.next()


async def load_zodiac_sign(message: types.Message,
                           state: FSMContext):
    async with state.proxy() as data:
        data['zodiac_sign'] = message.text

    await bot.send_message(
        chat_id=message.from_user.id,
        text='Send me your photo 📷\n'
             'only in photo format'
    )
    await RegistrationStates.next()


async def load_photo(message: types.Message,
                     state: FSMContext):
    db = bot_db.Database()
    path = await message.photo[-1].download(
        destination_dir=MEDIA_DESTINATION
    )

    async with state.proxy() as data:
        db.sql_insert_profile(
            tg_id=message.from_user.id,
            nickname=data['nickname'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            bio=data['bio'],
            age=data['age'],
            zodiac_sign=data['zodiac_sign'],
            photo=path.name
        )

        with open(path.name, 'rb') as photo:
            await bot.send_photo(
                chat_id=message.from_user.id,
                photo=photo,
                caption=const.PROFILE_TEXT.format(
                    nickname=data['nickname'],
                    first_name=data['first_name'],
                    last_name=data['last_name'],
                    bio=data['bio'],
                    age=data['age'],
                    zodiac_sign=data['zodiac_sign'],
                )
            )
    await bot.send_message(
            chat_id=message.from_user.id,
            text='You have successfully registered\n'
                 'Congrats!'
        )
    await state.finish()


def register_registration_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(
        registration_start,
        lambda call: call.data == 'registration'
    )
    dp.register_message_handler(
        load_nickname,
        state=RegistrationStates.nickname,
        content_types=['text']
    )
    dp.register_message_handler(
        load_first_name,
        state=RegistrationStates.first_name,
        content_types=['text']
    )
    dp.register_message_handler(
        load_last_name,
        state=RegistrationStates.last_name,
        content_types=['text']
    )
    dp.register_message_handler(
        load_bio,
        state=RegistrationStates.biography,
        content_types=['text']
    )
    dp.register_message_handler(
        load_age,
        state=RegistrationStates.age,
        content_types=['text']
    )
    dp.register_message_handler(
        load_zodiac_sign,
        state=RegistrationStates.zodiac_sign,
        content_types=['text']
    )
    dp.register_message_handler(
        load_photo,
        state=RegistrationStates.photo,
        content_types=types.ContentTypes.PHOTO
    )
