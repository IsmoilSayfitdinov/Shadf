import requests
import psycopg2
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
import time
import random
import asyncio

# Telegram API tokeni
API_TOKEN = '8155156574:AAGy4PpaXLrFyYsDMzDwAWIs286EhuZbfqs'

# PostgreSQL ma'lumotlar bazasi bilan ulanish parametrlari
DB_PARAMS = {
    'dbname': 'loginemaktab_db',  # o'zgartiring
    'user': 'loginemaktab',       # o'zgartiring
    'password':'Ismoil1233',  # o'zgartiring
    'host': 'postgresql-loginemaktab.alwaysdata.net',       # server manzili
    'port': '5432'             # PostgreSQL porti
}

# Boshlang'ich tugma
keyboardStart = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Royhatdan o'tish boshlash"),
            KeyboardButton(text="Foydalanuvchi qo'shish"),
        ],
        [
            KeyboardButton(text="Foydalanuvchi o'chirish"),
            KeyboardButton(text="Barcha foydalanuvchilarni ko'rish"),
        ]
        [
            KeyboardButton(text="Chiqish"),
        ]
    ],
    resize_keyboard=True
)

keyboardStart2 = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Royhatdan o'tish Oquvchilar"),
            KeyboardButton(text="Royhatdan o'tish Ota Onalar"),
        ],
        [
            KeyboardButton(text="Chiqish"),
        ]
    ],
    resize_keyboard=True
)



keyboardStart3 = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Oquvchilar"),
            KeyboardButton(text="Ota Onalar"),
        ],
        [
            KeyboardButton(text="Chiqish"),
        ],
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
def add_user_to_db(username, password):
    conn = psycopg2.connect(**DB_PARAMS)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (username, password) VALUES (%s, %s)
    ''', (username, password))
    conn.commit()
    conn.close()
    
def add_user_to_db2(username, password):
    conn = psycopg2.connect(**DB_PARAMS)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users2 (username, password) VALUES (%s, %s)
    ''', (username, password))
    conn.commit()
    conn.close()




# Ma'lumotlar bazasidan foydalanuvchini o'chirish
def delete_user_from_db(user_id):
    conn = psycopg2.connect(**DB_PARAMS)
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM users WHERE id = %s
    ''', (user_id,))
    conn.commit()
    conn.close()
    
    
def delete_user_from_db2(user_id):
    conn = psycopg2.connect(**DB_PARAMS)
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM users2 WHERE id = %s
    ''', (user_id,))
    conn.commit()
    conn.close()




# Ma'lumotlar bazasidan barcha foydalanuvchilarni olish
def start_register():
    conn = psycopg2.connect(**DB_PARAMS)
    cursor = conn.cursor()
    cursor.execute('SELECT username, password FROM users')
    users = cursor.fetchall()
    conn.close()
    return users

def start_register2():
    conn = psycopg2.connect(**DB_PARAMS)
    cursor = conn.cursor()
    cursor.execute('SELECT username, password FROM users2')
    users = cursor.fetchall()
    conn.close()
    return users



def get_all_users_from_db():
    conn = psycopg2.connect(**DB_PARAMS)
    cursor = conn.cursor()
    cursor.execute('SELECT id, username FROM users')
    users = cursor.fetchall()
    conn.close()
    return users

def get_all_users_from_db2():
    conn = psycopg2.connect(**DB_PARAMS)
    cursor = conn.cursor()
    cursor.execute('SELECT id, username FROM users2')
    users = cursor.fetchall()
    conn.close()
    return users

# Start komandasi uchun handler
@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.answer(
        "Royhatdan o'tishni boshlash uchun pastdagi tugmani bosing.",
        reply_markup=keyboardStart
    )
    
@dp.message(lambda message: message.text == "Royhatdan o'tish boshlash")
async def send_welcome2(message: types.Message):
    await message.answer(
        "Bitasini tanglang !!!.",
        reply_markup=keyboardStart2
    )

    @dp.message(lambda message: message.text == "Royhatdan o'tish Oquvchilar")
    async def handle_login_student(message: types.Message):
    # DBdan foydalanuvchilarni olish
        users = start_register()
        if users:
             for user in users:
                username, password = user
                login_data = {
                    'login': username,
                    'password': password
                }
                response = requests.post('https://login.emaktab.uz/', data=login_data)

                if response.status_code == 200:
                    await message.answer(f"{username} foydalanuvchisi ✅ 😃.")
                else:
                    await message.answer(f"{username} foydalanuvchisi ❌ ☹️")

                # Tasodifiy kutish
                time.sleep(random.uniform(1, 3))
        else:
            await message.answer("Foydalanuvchilar mavjud emas.")
    
    @dp.message(lambda message: message.text == "Royhatdan o'tish Ota Onalar")
    async def handle_login_student(message: types.Message):
    # DBdan foydalanuvchilarni olish
        users = start_register2()
        if users:
            for user in users:
                username, password = user
                login_data = {
                    'login': username,
                    'password': password
                }
                response = requests.post('https://login.emaktab.uz/', data=login_data)

                if response.status_code == 200:
                    await message.answer(f"{username} foydalanuvchisi ✅ 😃.")
                else:
                    await message.answer(f"{username} foydalanuvchisi ❌ ☹️")

                # Tasodifiy kutish
                time.sleep(random.uniform(1, 3))
        else:
            await message.answer("Foydalanuvchilar mavjud emas.")





# Foydalanuvchi qo'shish
@dp.message(lambda message: message.text == "Foydalanuvchi qo'shish")
async def start2(message: types.Message):
    await message.answer("Iltimos foydalanuvchini tanglang. ", reply_markup=keyboardStart3)
    
    @dp.message(lambda message: message.text == "Oquvchilar")
    async def handle_add_user(message: types.Message):
        await message.answer("Iltimos, username va parolni kiriting (format: username password).")
        # Foydalanuvchidan username va password so'raymiz
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
    async def handle_add_user(message: types.Message):
        await message.answer("Iltimos, username va parolni kiriting (format: username password).")
        # Foydalanuvchidan username va password so'raymiz
        @dp.message()
        async def add_user(message: types.Message):
            user_input = message.text.split()
            if len(user_input) != 2:
                await message.answer("Iltimos, to'g'ri formatda kiriting: username password.")
                return
            
            username, password = user_input
            add_user_to_db2(username, password)
            await message.answer(f"{username} foydalanuvchisi bazaga qo'shildi.")

    


# Foydalanuvchi o'chirish
@dp.message(lambda message: message.text == "Foydalanuvchi o'chirish")
async def start3(message: types.Message):
    await message.answer("Iltimos, qo'shishni istagan foydalanuvchini tanglang. ", reply_markup=keyboardStart3)
    
    
    @dp.message(lambda message: message.text == "Oquvchilar")
    async def handle_delete_user(message: types.Message):
        await message.answer("Iltimos, o'chirishni istagan foydalanuvchining ID sini kiriting.")
        
        # Foydalanuvchidan id so'raymiz
        @dp.message()
        async def delete_user(message: types.Message):
            try:
                user_id = int(message.text)
                users = get_all_users_from_db()
                user_exists = False
                
                # Foydalanuvchini tekshiramiz
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
    async def handle_delete_user(message: types.Message):
        await message.answer("Iltimos, o'chirishni istagan foydalanuvchining ID sini kiriting.")
        
        # Foydalanuvchidan id so'raymiz
        @dp.message()
        async def delete_user(message: types.Message):
            try:
                user_id = int(message.text)
                users = get_all_users_from_db()
                user_exists = False
                
                # Foydalanuvchini tekshiramiz
                for user in users:
                    if user[0] == user_id:
                        delete_user_from_db2(user_id)
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
    users2 = get_all_users_from_db2()
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


@dp.message(lambda message: message.text == "Chiqish")
async def handle_exit(message: types.Message):
    await message.answer("Botdan chiqib ketildi.", reply_markup=keyboardStart)


# Asinxron ishga tushirish
async def main():
    create_db()  # Ma'lumotlar bazasini yaratish
    bot = Bot(token=API_TOKEN)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
