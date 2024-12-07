from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.context import FSMContext
import pandas as pd
import psycopg2
import requests
import asyncio
import random
import os


API_TOKEN = '8155156574:AAGy4PpaXLrFyYsDMzDwAWIs286EhuZbfqs'

DB_PARAMS = {
    'dbname': 'maktab',  # o'zgartiring
    'user': 'postgres',   # o'zgartiring
    'password': '9312',   # o'zgartiring
    'host': 'localhost',  # server manzili
    'port': '5432'        # PostgreSQL porti
}

keyboardStart = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Royhatdan o'tish boshlash ⏩")],
        [KeyboardButton(text="O'quvchi Qo'shish ➕")],
        [KeyboardButton(text="Ota Ona Qo'shish ➕")],
        [KeyboardButton(text="O'quvchi O'chirish ➖")],
        [KeyboardButton(text="Ota Ona O'chirish ➖")],
        [KeyboardButton(text="O'quvchi Yangilash 🔄")],
        [KeyboardButton(text="Ota Ona Yangilash 🔄")],
        [KeyboardButton(text="Excel orqali O'quvchilar Qo'shish 📄")],
        [KeyboardButton(text="Excel orqali Ota-onalar Qo'shish 📄")],
        [KeyboardButton(text="Barcha foydalanuvchilarni ko'rish 👀")],
        [KeyboardButton(text="Barcha O'quvchilarni O'chirish 🗑")],  # Yangi tugma
        [KeyboardButton(text="Barcha Ota-Onalarni O'chirish 🗑")],
        [KeyboardButton(text="Foydalanuvchini qidirish 🔍")]
    ],
    resize_keyboard=True
)

keyboardStart2 = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Royhatdan o'tish o'quvchilar ⏩")],
        [KeyboardButton(text="Royhatdan o'tish ota-ona ➕")],
        [KeyboardButton(text="Chiqish 🚪")],
    ],
    resize_keyboard=True
)



bot = Bot(token=API_TOKEN)
dp = Dispatcher()

class UserState(StatesGroup):
    adding_student = State()  # O'quvchi qo'shish
    adding_parent = State()   # Ota-ona qo'shish
    deleting_student = State()  # O'quvchi o'chirish
    deleting_parent = State()   # Ota-ona o'chirish
    updating_student = State()
    updating_parent = State()
    uploading_excel = State()
    searching_user = State()

def get_db_connection():
    return psycopg2.connect(**DB_PARAMS)

def execute_query(query, params=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()

def fetch_query(query, params=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    result = cursor.fetchall()
    conn.close()
    return result

def create_db():
    create_users_table = '''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    '''
    create_users2_table = '''
        CREATE TABLE IF NOT EXISTS users2 (
            id SERIAL PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    '''
    execute_query(create_users_table)
    execute_query(create_users2_table)

def add_user_to_db(username, password, table='users'):
    query = f"INSERT INTO {table} (username, password) VALUES (%s, %s)"
    execute_query(query, (username, password))

def delete_user_from_db(user_id, table='users'):
    query = f"DELETE FROM {table} WHERE id = %s"
    execute_query(query, (user_id,))

def get_all_users_from_db(table='users'):
    query = f"SELECT id, username, password FROM {table}"
    return fetch_query(query)



login_counter = 0
MAX_LOGIN_COUNT = 120
WAIT_TIME_SECONDS = 100

login_counter_parent = 0
MAX_LOGIN_COUNT_PARENT = 120
WAIT_TIME_SECONDS_PARENT = 100





@dp.message(F.text == "Royhatdan o'tish o'quvchilar ⏩")  # Foydalanuvchi "student_login" deb yozganida
async def handle_login_student(message: types.Message):
    global login_counter
    users = get_all_users_from_db('users')
    if users:
        for user in users:
            id, username, password = user
            login_data = {'login': username, 'password': password}
            response = requests.post('https://login.emaktab.uz/', data=login_data)
            if response.status_code == 200:
                await message.answer(f"ID: {id} - {username} foydalanuvchisi ✅ 😃.")
            else:
                await message.answer(f"ID: {id} - {username} foydalanuvchisi ❌ ☹️")
            
            login_counter += 1
            
            if login_counter >= MAX_LOGIN_COUNT:
                await message.answer("120 ta foydalanuvchi login qilindi. Bot 100 soniya dam oladi va yana ishga tushadi 😊.")
                await asyncio.sleep(WAIT_TIME_SECONDS)
                login_counter = 0
            await asyncio.sleep(random.uniform(1, 2))  # Tasodifiy kutish
    else:
        await message.answer("Talabalar mavjud emas.")

# Ota-onalar uchun login funksiyasi
@dp.message(F.text == "Royhatdan o'tish ota-ona ➕")  # Foydalanuvchi "parent_login" deb yozganida
async def handle_login_parent(message: types.Message):
    global login_counter_parent
    users = get_all_users_from_db('users2')
    if users:
        for user in users:
            id, username, password = user
            login_data = {'login': username, 'password': password}
            response = requests.post('https://login.emaktab.uz/', data=login_data)
            
            if response.status_code == 200:
                await message.answer(f"ID : {id} - {username} foydalanuvchisi ✅ 😃.")
            else:
                await message.answer(f"ID: {id} - {username} foydalanuvchisi ❌ ☹️")
            
            login_counter_parent += 1
            
            if login_counter_parent >= MAX_LOGIN_COUNT_PARENT:
                await message.answer("120 ta foydalanuvchi login qilindi. Bot 100 soniya dam oladi va yana ishga tushadi 😊.")
                await asyncio.sleep(WAIT_TIME_SECONDS_PARENT)
                login_counter_parent = 0
            
            await asyncio.sleep(random.uniform(2, 4))  # Tasodifiy kutish
    else:
        await message.answer("Ota-onalar mavjud emas.")
    
    

@dp.message(F.text == "O'quvchi Yangilash 🔄")
async def handle_update_student(message: types.Message, state: FSMContext):
    await message.answer("Iltimos, yangilash uchun o'quvchining ID sini, yangi username va yangi parolni kiriting (format: ID username password).")
    await state.set_state(UserState.updating_student)


@dp.message(StateFilter(UserState.updating_student))
async def update_student(message: types.Message, state: FSMContext):
    try:
        user_id, username, password = message.text.strip().split()
        execute_query("UPDATE users SET username = %s, password = %s WHERE id = %s", (username, password, user_id))
        await message.answer(f"O'quvchi ID: {user_id} muvaffaqiyatli yangilandi.")
    except Exception as e:
        await message.answer(f"Xatolik: {str(e)}")
    finally:
        await state.clear()


@dp.message(F.text == "Ota Ona Yangilash 🔄")
async def handle_update_parent(message: types.Message, state: FSMContext):
    await message.answer("Iltimos, yangilash uchun ota-onaning ID sini, yangi username va yangi parolni kiriting (format: ID username password).")
    await state.set_state(UserState.updating_parent)

@dp.message(StateFilter(UserState.updating_parent))
async def update_parent(message: types.Message, state: FSMContext):
    try:
        user_id, username, password = message.text.strip().split()
        execute_query("UPDATE users2 SET username = %s, password = %s WHERE id = %s", (username, password, user_id))
        await message.answer(f"Ota-ona ID: {user_id} muvaffaqiyatli yangilandi.")
    except Exception as e:
        await message.answer(f"Xatolik: {str(e)}")
    finally:
        await state.clear()
        
@dp.message(F.text == "Excel orqali O'quvchilar Qo'shish 📄")
@dp.message(F.text == "Excel orqali Ota-onalar Qo'shish 📄")
async def handle_excel_upload(message: types.Message, state: FSMContext):
    if "O'quvchilar" in message.text:
        role = "users"
        why = "O'quvchilar"
    else:
        role = "users2"
        why = "Ota-onalar" 

    await message.answer(f"{role.capitalize()} \n Iltimos, Excel faylni yuboring (faqat .xlsx formatdagi fayl qabul qilinadi).")
    await state.set_state(UserState.uploading_excel)  # Holatni o'rnatish
    await state.update_data(role=role, why=why)  # role ni saqlash

@dp.message(StateFilter(UserState.uploading_excel), F.content_type == 'document')
async def process_excel_upload(message: types.Message, state: FSMContext):
    try:
        data = await state.get_data()
        role = data.get("role", "users")  # role ni olish
        why = data.get("why", "O'quvchilar")
        
        file_id = message.document.file_id
        file = await bot.get_file(file_id)
        file_path = file.file_path
        file_name = f"./{message.document.file_name}" 
        await bot.download_file(file_path, f"./{message.document.file_name}")

        # Excel faylini o'qish
        df = pd.read_excel(f"./{message.document.file_name}")

        # NaN qiymatlarini olib tashlash
        df = df.dropna(axis=1, how='all')  # Agar ustunda faqat NaN bo'lsa, ustunni o'chirish
        df = df.dropna(subset=['Unnamed: 1', 'Unnamed: 2'])  # username va table ustunlarini tekshirish

        # Ustun nomlarini to'g'irlash (faqat 2 ta ustun bor)
        df.columns = ['username', 'password']  # Faol ustunlar faqat 'username' va 'password' bo'lsin

        # NaN qiymatlarini olib tashlash (agar username yoki password yo'q bo'lsa)
        df = df.dropna(subset=['username', 'password'])

        # Ma'lumotlarni o'qib bazaga kiritish
        for index, row in df.iterrows():
            username = row['username']
            password = row['password']

            # Debug: Exceldan olingan ma'lumotlarni tekshirish
            print(f"Username: {username}, Password: {password}")

            # Foydalanuvchi bazada mavjudligini tekshirish
            check_query = f"SELECT COUNT(*) FROM {role} WHERE username = %s"
            
            # DB ulanishi va cursor yaratish
            connection = get_db_connection()  # Bu yerda get_db_connection() ulanishni qaytaradi
            cursor = connection.cursor()  # Cursor yaratish
            
            cursor.execute(check_query, (username,))
            result = cursor.fetchone()

            if result and result[0] > 0:
                # Agar foydalanuvchi bazada mavjud bo'lsa
                print(f"{username} bazada mavjud. Yana qo'shilmadi.")
                await message.answer(f"{username} bazada mavjud. Yana qo'shilmadi.")
                cursor.close()
                connection.close()  # Cursor va connectionni yopish
                continue  # Keyingi foydalanuvchiga o'tish

            # Foydalanuvchi bazaga qo'shish
            insert_query = f"INSERT INTO {role} (username, password) VALUES (%s, %s)"
            cursor.execute(insert_query, (username, password))  # Ma'lumotlarni qo'shish
            connection.commit()  # O'zgarishlarni saqlash
            
            print(f"{username} muvaffaqiyatli qo'shildi.")
            cursor.close()
            connection.close()  # Cursor va connectionni yopish
        
        await message.answer(f"{why.capitalize()} muvaffaqiyatli qo'shildi.")
        
        os.remove(file_name) 
    except Exception as e:
        await message.answer(f"Xatolik: {str(e)}")
    finally:
        await state.clear()



@dp.message(F.text == "Barcha O'quvchilarni O'chirish 🗑")
async def delete_all_students(message: types.Message):
    try:
        # 'users' jadvalidan barcha ma'lumotlarni o'chirish
        query = "DELETE FROM users"  # Jadvalni nomini to'g'ri kiriting
        execute_query(query)  # Bu yerda query bajariladi
        await message.answer("Barcha o'quvchilar muvaffaqiyatli o'chirildi.")
    except Exception as e:
        await message.answer(f"Xatolik: {str(e)}")

@dp.message(F.text == "Barcha Ota-Onalarni O'chirish 🗑")
async def delete_all_parents(message: types.Message):
    try:
        # 'users2' jadvalidan barcha ma'lumotlarni o'chirish
        query = "DELETE FROM users2"  # Jadvalni nomini to'g'ri kiriting
        execute_query(query)  # Bu yerda query bajariladi
        await message.answer("Barcha ota-onalar muvaffaqiyatli o'chirildi.")
    except Exception as e:
        await message.answer(f"Xatolik: {str(e)}")


@dp.message(F.text == "Foydalanuvchini qidirish 🔍")
async def start_searching_user(message: types.Message, state: FSMContext):
    await message.answer("Iltimos, qidiruv uchun username kiriting.")
    await state.set_state(UserState.searching_user)

@dp.message(StateFilter(UserState.searching_user))
async def search_user(message: types.Message, state: FSMContext):
    username = message.text.strip()
    
    # Qidirish uchun DBdan ma'lumot olish
    query = "SELECT id, username FROM users WHERE username = %s"
    result = fetch_query(query, (username,))
    
    if result:
        # Foydalanuvchi topildi
        user_info = "\n".join([f"ID: {user[0]}, Username: {user[1]}" for user in result])
        await message.answer(f"Topilgan foydalanuvchilar:\n{user_info}")
    else:
        await message.answer("Foydalanuvchi topilmadi.")
    
    await state.clear()  # State ni tozalash


            
@dp.message(F.text == "Chiqish 🚪")
async def handle_exit(message: types.Message):
    await message.answer("Boshlash uchun pastdagi tugmalrni birini bosing !!", reply_markup=keyboardStart)

@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.answer("Royhatdan o'tishni boshlash uchun pastdagi tugmani bosing.", reply_markup=keyboardStart)

@dp.message(F.text == "Royhatdan o'tish boshlash ⏩")
async def send_welcome2(message: types.Message):
    await message.answer("Bitasini tanglang !!!", reply_markup=keyboardStart2)

@dp.message(F.text == "O'quvchi Qo'shish ➕")
async def handle_add_student(message: types.Message, state: FSMContext):
    await message.answer("Iltimos, o'quvchi username va parolni kiriting (format: username password).")
    await state.set_state(UserState.adding_student)

@dp.message(StateFilter(UserState.adding_student), lambda message: len(message.text.strip().split()) == 2)
async def add_student_to_db(message: types.Message, state: FSMContext):
    username, password = message.text.strip().split()
    add_user_to_db(username, password)
    await message.answer(f"{username} o'quvchisi muvaffaqiyatli bazaga qo'shildi.")
    await state.clear()

@dp.message(F.text == "Ota Ona Qo'shish ➕")
async def handle_add_parent(message: types.Message, state: FSMContext):
    await message.answer("Iltimos, ota-ona username va parolni kiriting (format: username password).")
    await state.set_state(UserState.adding_parent)

@dp.message(StateFilter(UserState.adding_parent), lambda message: len(message.text.strip().split()) == 2)
async def add_parent_to_db(message: types.Message, state: FSMContext):
    username, password = message.text.strip().split()
    add_user_to_db(username, password, table='users2')
    await message.answer(f"{username} ota-onasi muvaffaqiyatli bazaga qo'shildi.")
    await state.clear()

@dp.message(F.text == "O'quvchi O'chirish ➖")
async def handle_delete_student(message: types.Message, state: FSMContext):
    await message.answer("Iltimos, o'chirishni istagan o'quvchining ID sini kiriting.")
    await state.set_state(UserState.deleting_student)

@dp.message(StateFilter(UserState.deleting_student), lambda message: message.text.isdigit())
async def delete_student_from_db(message: types.Message, state: FSMContext):
    user_id = int(message.text)
    users = get_all_users_from_db()
    if any(user[0] == user_id for user in users):
        delete_user_from_db(user_id)
        await message.answer(f"ID: {user_id} bo'lgan o'quvchi o'chirildi.")
    else:
        await message.answer(f"ID: {user_id} bo'lgan o'quvchi mavjud emas.")
    await state.clear()

@dp.message(F.text == "Ota Ona O'chirish ➖")
async def handle_delete_parent(message: types.Message, state: FSMContext):
    await message.answer("Iltimos, o'chirishni istagan ota-onaning ID sini kiriting.")
    await state.set_state(UserState.deleting_parent)

@dp.message(StateFilter(UserState.deleting_parent), lambda message: message.text.isdigit())
async def delete_parent_from_db(message: types.Message, state: FSMContext):
    user_id = int(message.text)
    users = get_all_users_from_db(table='users2')
    if any(user[0] == user_id for user in users):
        delete_user_from_db(user_id, table='users2')
        await message.answer(f"ID: {user_id} bo'lgan ota-ona o'chirildi.")
    else:
        await message.answer(f"ID: {user_id} bo'lgan ota-ona mavjud emas.")
    await state.clear()

async def send_long_message(message: types.Message, text: str):
    max_length = 4096  # Maksimal uzunlik
    for i in range(0, len(text), max_length):
        await message.answer(text[i:i+max_length])


@dp.message(F.text == "Barcha foydalanuvchilarni ko'rish 👀")
async def handle_show_all_users(message: types.Message):
    users = get_all_users_from_db()
    users2 = get_all_users_from_db(table='users2')
    
    user_list = ""
    parent_list = ""
    
    if users:
        user_list = "\n".join([f"ID: {user[0]} - Username: {user[1]}" for user in users])
    else:
        user_list = "O'quvchilar mavjud emas."

    if users2:
        parent_list = "\n".join([f"ID: {user[0]} - Username: {user[1]}" for user in users2])
    else:
        parent_list = "Ota-onalar mavjud emas."

    # Foydalanuvchilar ro'yxatini bo'lib yuborish
    if user_list:
        await send_long_message(message, f"Barcha Oquvchilar:\n\n{user_list}")

    if parent_list:
        await send_long_message(message, f"Barcha Ota-onalar:\n\n{parent_list}")




@dp.message(F.text == "Royhatdan o'tish o'quvchilar ⏩")
async def start_register_students(message: types.Message):
    await handle_login_student(message)

@dp.message(F.text == "Royhatdan o'tish ota-ona ➕")
async def start_register_parents(message: types.Message):
    await handle_login_parent(message)



async def main():
    create_db()  # Ma'lumotlar bazasini yaratish
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
