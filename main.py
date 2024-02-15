from aiogram import executor
from config import dp
from handlers import (
    start,
)

start.register_start_handlers(dp=dp)


if __name__ == "__main__":
    executor.start_polling(
        dp
    )
