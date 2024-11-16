
import asyncio
import logging
import json 

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

import ai_model

API_TOKEN = '7911900370:AAH8I5skyucy8wXUXPYLB4x3tNsgl0CJxiE'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher() 

user_choices = {}

async def process_pc_build(message: types.Message):
    await message.reply("Вы выбрали режим сборки ПК. Напишите ваши требования к ПК (повседневные задачи) и я соберу вам все необходимые комплекутющие.")

async def process_select_laptop(message: types.Message):
    await message.reply("Вы выбрали режим подбора ноутбука. Напишите ваши требования к ноутбуку и я соберу вам подборку подходящих для вас ноутбуков.")

def beautify_message(ai_response):
    if(ai_response.startswith("```json")):
        ai_response = ai_response.replace("```json", "")
        ai_response = ai_response.replace("```", "")
    ai_response = json.loads(ai_response)
    items_size = len(ai_response["items"])
    if (items_size) == 0:
        return ai_response["description"]
    
    return_message = f"{ai_response["description"]} \n\n"
    
    for i in range(items_size):
        name = ai_response["items"][i]["name"]
        description = ai_response["items"][i]["description"]
        price = ai_response["items"][i]["price"]
        return_message += f"{i+1}. {name} - {description} - {price}\n"
    return return_message

def main_kb(user_telegram_id: int):
    kb_list = [
        [KeyboardButton(text="О нас"), KeyboardButton(text="Помощь")],
        [KeyboardButton(text="Сборка ПК"), KeyboardButton(text="Подбор ноутбука")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
    return keyboard


@dp.message(F.text == 'start')  
async def cmd_start(message):
    await message.answer('Запуск сообщения по команде /start используя фильтр CommandStart()',
                         reply_markup=main_kb(message.from_user.id))


@dp.message()
async def handle_message(message: types.Message):
    user_id = message.from_user.id

    if message.text == "Сборка ПК":
        user_choices[user_id] = "pc-build"
        await process_pc_build(message)
    elif message.text == "Подбор ноутбука":
        user_choices[user_id] = "select-laptop"
        await process_select_laptop(message)
    elif user_id in user_choices:
        ai_response = ai_model.get_response(user_choices[user_id], message.text)
        await message.reply(beautify_message(ai_response))


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())