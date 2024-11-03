
import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types \
        import Message, InlineKeyboardButton, \
                InlineKeyboardMarkup, CallbackQuery


import ai_model

TOKEN = "7911900370:AAH8I5skyucy8wXUXPYLB4x3tNsgl0CJxiE"
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    hello_message = "Здравствуйте, я бот, который помогает людям собирать настольный компьютер или выбирать ноутбук в зависимости от потребностей. Вы можете написать мне короткое сообщение о том, чем занимаетесь, и я помогу вам с выбором."
    await message.answer(hello_message)


@dp.message()
async def echo_handler(message: Message) -> None:
    try:
        response = ai_model.get_response(message.text)
        await message.answer(response)
    except TypeError:
        await message.answer("Nice try!")


async def main() -> None:
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

