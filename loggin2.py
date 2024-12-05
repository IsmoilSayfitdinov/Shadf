import requests
import psycopg2
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
import asyncio
import time
import random

# Telegram API tokeni
API_TOKEN = '8155156574:AAGy4PpaXLrFyYsDMzDwAWIs286EhuZbfqs'

# PostgreSQL ma'lumotlar bazasi bilan ulanish parametrlari
DB_PARAMS = {
    'dbname': 'loginemaktab_db',
    'user': 'loginemaktab',
    'password': 'Ismoil1233',
    'host': 'postgresql-loginemaktab.alwaysdata.net',
    'port': '5432'
}

# Boshlang'ich tugma
keyboardStart = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Royhatdan o'tish boshlash"),
         KeyboardButton(text="Foydalanuvchi qo'shish")],
        [KeyboardButton(text="Foydalanuvchi o'chirish"),
         KeyboardButton(text="Barcha foydalanuvchilarni ko'rish")],
        [KeyboardButton(text="Chiqish")],
    ],
    resize_keyboard=True
)

keyboardStart2 = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Royhatdan o'tish Oquvchilar"),
         KeyboardButton(text="Royhatdan o'tish Ota Onalar")],
        [KeyboardButton(text="Chiqish")],
    ],
    resize_keyboard=True
)

keyboardStart3 = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Oquvchilar"),
         KeyboardButton(text="Ota Onalar")],
        [KeyboardButton(text="Chiqish")],
    ],
    resize_keyboard=True
)

# Dispatcher va Bot obyektlari
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# PostgreSQL ma'lumotlar bazasiga ulanish va kerakli jadvalni yaratish
def create_db():
    conn = psycopg2.connect(**DB_PARAMS)
    cursor = conn.cursor()
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS users2 (
            id SERIAL PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Ma'lumotlar bazasiga foydalanuvchi qo'shish
def add_user_to_db(username, password, table='users'):
    conn = psycopg2.connect(**DB_PARAMS)
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO {table} (username, password) VALUES (%s, %s)", (username, password))
    conn.commit()
    conn.close()

# Ma'lumotlar bazasidan foydalanuvchini o'chirish
def delete_user_from_db(user_id, table='users'):
    conn = psycopg2.connect(**DB_PARAMS)
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM {table} WHERE id = %s", (user_id,))
    conn.commit()
    conn.close()

# Ma'lumotlar bazasidan barcha foydalanuvchilarni olish
def get_all_users_from_db(table='users'):
    conn = psycopg2.connect(**DB_PARAMS)
    cursor = conn.cursor()
    cursor.execute(f"SELECT id, username FROM {table}")
    users = cursor.fetchall()
    conn.close()
    return users

# Start komandasi uchun handler
@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.answer("Royhatdan o'tishni boshlash uchun pastdagi tugmani bosing.", reply_markup=keyboardStart)

@dp.message(lambda message: message.text == "Royhatdan o'tish boshlash")
async def send_welcome2(message: types.Message):
    await message.answer("Bitasini tanglang !!!.", reply_markup=keyboardStart2)

# Foydalanuvchi qo'shish
@dp.message(lambda message: message.text == "Foydalanuvchi qo'shish")
async def handle_add_user(message: types.Message):
    await message.answer("Iltimos foydalanuvchini tanglang. ", reply_markup=keyboardStart3)

@dp.message(lambda message: message.text == "Oquvchilar")
async def handle_add_user_students(message: types.Message):
    await message.answer("Iltimos, username va parolni kiriting (format: username password).")
    
    @dp.message()
    async def add_user(message: types.Message):
        user_input = message.text.split()
        if len(user_input) != 2:
            await message.answer("Iltimos, to'g'ri formatda kiriting: username password.")
            return
        
        username, password = user_input
        add_user_to_db(username, password)
        await message.answer(f"{username} foydalanuvchisi bazaga qo'shildi.")

@dp.message(lambda message: message.text == "Ota Onalar")
async def handle_add_user_parents(message: types.Message):
    await message.answer("Iltimos, username va parolni kiriting (format: username password).")
    
    @dp.message()
    async def add_user(message: types.Message):
        user_input = message.text.split()
        if len(user_input) != 2:
            await message.answer("Iltimos, to'g'ri formatda kiriting: username password.")
            return
        
        username, password = user_input
        add_user_to_db(username, password, table='users2')
        await message.answer(f"{username} foydalanuvchisi bazaga qo'shildi.")

# Foydalanuvchi o'chirish
@dp.message(lambda message: message.text == "Foydalanuvchi o'chirish")
async def start3(message: types.Message):
    await message.answer("Iltimos, qo'shishni istagan foydalanuvchini tanglang. ", reply_markup=keyboardStart3)

@dp.message(lambda message: message.text == "Oquvchilar")
async def handle_delete_user_students(message: types.Message):
    await message.answer("Iltimos, o'chirishni istagan foydalanuvchining ID sini kiriting.")
    
    @dp.message()
    async def delete_user(message: types.Message):
        try:
            user_id = int(message.text)
            users = get_all_users_from_db()
            user_exists = False
            
            for user in users:
                if user[0] == user_id:
                    delete_user_from_db(user_id)
                    await message.answer(f"Ismi: {user[1]} bo'lgan foydalanuvchi o'chirildi.")
                    user_exists = True
                    break

            if not user_exists:
                await message.answer(f"Ismi: {user_id} bo'lgan foydalanuvchi mavjud emas.")
        except ValueError:
            await message.answer("Iltimos, faqat raqamlarni kiriting.")

@dp.message(lambda message: message.text == "Ota Onalar")
async def handle_delete_user_parents(message: types.Message):
    await message.answer("Iltimos, o'chirishni istagan foydalanuvchining ID sini kiriting.")
    
    @dp.message()
    async def delete_user(message: types.Message):
        try:
            user_id = int(message.text)
            users = get_all_users_from_db(table='users2')
            user_exists = False
            
            for user in users:
                if user[0] == user_id:
                    delete_user_from_db(user_id, table='users2')
                    await message.answer(f"Ismi: {user[1]} bo'lgan foydalanuvchi o'chirildi.")
                    user_exists = True
                    break

            if not user_exists:
                await message.answer(f"Ismi: {user_id} bo'lgan foydalanuvchi mavjud emas.")
        except ValueError:
            await message.answer("Iltimos, faqat raqamlarni kiriting.")

# Barcha foydalanuvchilarni ko'rsatish
@dp.message(lambda message: message.text == "Barcha foydalanuvchilarni ko'rish")
async def handle_show_all_users(message: types.Message):
    users = get_all_users_from_db()
    users2 = get_all_users_from_db(table='users2')
    
    if users:
        user_list = "\n".join([f"ID: {user[0]} - Username: {user[1]}" for user in users])
        await message.answer(f"Barcha Oquvchilar:\n\n{user_list}")
    else:
        await message.answer("Hozirda Oquvchilar mavjud emas.")
    
    if users2:
        user_list2 = "\n".join([f"ID: {user[0]} - Username: {user[1]}" for user in users2])
        await message.answer(f"Barcha Ota Onalar:\n\n{user_list2}")
    else:
        await message.answer("Hozirda Ota Onalar mavjud emas.")

# Asosiy ishga tushurish
async def main():
    create_db()
    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())
