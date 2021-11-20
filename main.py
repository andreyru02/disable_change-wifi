from time import sleep
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
from auth import authentication
import json

with open('config.json', encoding='utf-8') as file:
    data = json.load(file)
    token = data.get('data').get('token')
    user_id = data.get('data').get('user_id')
    inet_login = data.get('data').get('inet_login')
    inet_password = data.get('data').get('inet_password')
    mac = data.get('data').get('mac')

bot = Bot(token=token)
dp = Dispatcher(bot)

keyboard = InlineKeyboardMarkup(row_width=2)
disable_wifi = InlineKeyboardButton(text='Отключить WiFi', callback_data="disable-wifi")
connect_sik = InlineKeyboardButton(text='Подключиться к SIK', callback_data="connect-sik")
connect_talakan = InlineKeyboardButton(text='Подключиться к TalakanOnline', callback_data="connect-talakan")
keyboard.add(disable_wifi, connect_sik, connect_talakan)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    if message.from_user.id == int(user_id):
        await bot.send_message(message.from_user.id, 'Выберите действие:', reply_markup=keyboard)


@dp.callback_query_handler()
async def menu(call: types.CallbackQuery):
    if call.data == 'disable-wifi':
        await bot.send_message(call.from_user.id, 'WiFi отключен!')
        os.system("nmcli radio wifi off")
    elif call.data == 'connect-sik':
        await bot.send_message(call.from_user.id, 'Подключено к SIK!')
        os.system("nmcli c up SIK")
    elif call.data == 'connect-talakan':
        await bot.send_message(call.from_user.id, 'Подключено к TalakanOnline!')
        os.system("nmcli c up TalakanOnline")
        sleep(5)
        authentication(inet_login=inet_login, inet_password=inet_password, mac=mac)  # выполняем авторизацию
    else:
        await bot.send_message(call.from_user.id, 'Неизвестная команда!', reply_markup=keyboard)


if __name__ == '__main__':
    executor.start_polling(dp)
