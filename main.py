
import asyncio
import logging
import json 

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,\
            InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums.parse_mode import ParseMode
from aiogram.handlers import CallbackQueryHandler

import ai_model
import database
import parser

API_TOKEN = '7911900370:AAH8I5skyucy8wXUXPYLB4x3tNsgl0CJxiE'

logging.basicConfig(level=logging.INFO)
db = database.DB()

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
        url = parser.parse(name)
        description = ai_response["items"][i]["description"]
        price = ai_response["items"][i]["price"]
        return_message += f"{i+1}. [{name}]({url}) - {description} - {price} рублей\n"

    return_message += "\nВы можете оставить оценку подберке с помощью кнопок ниже."
    return return_message

def main_kb():
    kb_list = [
        [KeyboardButton(text="О нас"), KeyboardButton(text="Помощь")],
        [KeyboardButton(text="Сборка ПК"), KeyboardButton(text="Подбор ноутбука")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
    return keyboard


@dp.message(CommandStart())   
async def cmd_start(message):
    try:
        pass
        db.create_user(message.from_user.id,message.from_user.username)
    except Exception as e:
        print(f"Failed because {e}")
    
    await message.answer('Привет, я ассистент, который может помочь вам собрать компьютер или подобрать ноутбук по вашим нуждам. Все что вам нужно сделать - это выбрать режим и написать ваши требования.',
                        reply_markup=main_kb())


@dp.message(F.text == 'О нас')  
async def cmd_start(message):
    await message.answer("Наша команда разработчиков: \nБастриков Вячеслав - тимлид \nВоронин Николай - Аналитик \nОсипов Антон - Разработчик \nРайх Татьяна - Аналитик", 
                         reply_markup=main_kb())

@dp.message(F.text == 'Помощь')  
async def cmd_start(message):
    await message.answer("*Работа с ботом:* \nЯ могу помочь вам собрать компьютер или подобрать ноутбук по вашим нуждам\. \nВсе что вам нужно сделать \- это выбрать режим работы \(сборка компьютера или подбор ноутбука\) и написать ваши требования\.", 
                         reply_markup=main_kb(), parse_mode=ParseMode.MARKDOWN)


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
        responseId = db.insert_response(message.from_user.id, message.text, ai_response)
        
        inline_buttons = [[]]
        for i in range(1,6):
            inline_buttons[0].append(InlineKeyboardButton(text=str(i), callback_data=f'review_response_{1}_{i}'))
            inline_buttons[0].append(InlineKeyboardButton(text=str(i), callback_data=f'review_response_{responseId}_{i}'))

        beutify_msg = beautify_message(ai_response)
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=inline_buttons)
        await message.reply(beutify_msg, reply_markup=keyboard, parse_mode="Markdown")

async def review_response(callback_query: types.CallbackQuery):
    responseId, rating = callback_query.data.split("_")[-2:]
    if rating.isdigit():
        rating = int(rating)
    print(callback_query.from_user.id, responseId, rating, "")
    db.insert_rating(callback_query.from_user.id, responseId, rating, "")
    await callback_query.answer("Спасибо что оценили данную подборку")



async def main():
    dp.callback_query.register(review_response, lambda c: c.data and c.data.startswith('review_response'))
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())