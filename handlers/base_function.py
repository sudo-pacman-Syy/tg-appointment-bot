from aiogram.types import Message,CallbackQuery
from aiogram.filters import CommandStart,Command
from aiogram import Router,F
import sys 
from hendller import keyboard as kb
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup,State
import aiosqlite

my_router = Router(name=__name__)

class Book(StatesGroup):
    book_strijka = State()
    book_masaj = State()
    book_manikyur = State()
    book_name = State()
    book_date = State()


async def create_table():
    async with aiosqlite.connect("menegers_Books.db") as db:
        await db.execute("""CREATE TABLE IF NOT EXISTS Books(
  user_id INTEGER,
  service_type TEXT,
  name_specialist TEXT,
  data_book TEXT)""")
        await db.commit()
        

async def password_sql(user_id,service_type,name_specialist,data_book):
    await create_table()

    async with aiosqlite.connect("menegers_Books.db") as db:
        await db.execute("INSERT INTO Books(user_id,service_type,name_specialist,data_book) VALUES (?,?,?,?)",(user_id,service_type,name_specialist,data_book,))
        await db.commit()






@my_router.message(CommandStart())
async def command_start(message:Message):
    await message.answer("Добро пожаловать в бот для бронирования услуг!",reply_markup=kb.main_keyboard)

@my_router.message(F.text =="забранировать услугу!")
async def book(message:Message):
    await message.answer("отлична! выберите улсугу которую хотите забранировать!",reply_markup=kb.main_inlne)

@my_router.callback_query(F.data == "manikyur")
async def manikur(callback: CallbackQuery,state:FSMContext):
    await state.set_state(Book.book_manikyur)
    await state.update_data(book_type="Маникюр")
    await state.set_state(Book.book_name)
    await callback.message.answer("отличный выбор! выберите специалиста",reply_markup=kb.main_name)


@my_router.callback_query(F.data == "back",Book.book_name)
async def back_command(callback:CallbackQuery):
    await callback.message.edit_text("отлична! выберите улсугу которую хотите забранировать!",reply_markup=kb.main_inlne)
     
@my_router.callback_query(F.data.in_(["Egoe", "Grisha", "Artem"]),Book.book_name)
async def handle_names(callback: CallbackQuery,state:FSMContext):
    await state.update_data(book_name = callback.data)
    await state.set_state(Book.book_date)
    await callback.message.answer("отличный выбор специалиста! теперь выберите время.",reply_markup=kb.main_date)

@my_router.callback_query(F.data == "bez_raznici",Book.book_name)
async def handle_data(callback: CallbackQuery, state: FSMContext):
    await state.update_data(book_name="любой специалист")
    await state.set_state(Book.book_date)
    await callback.message.answer("Мы ручаемся за каждого специалиста! Теперь выберите время.",reply_markup=kb.main_date)


@my_router.callback_query(F.data == "massaj")
async def manikur(callback: CallbackQuery,state:FSMContext):
    await state.set_state(Book.book_masaj)
    await state.update_data(book_type="Массаж")
    await state.set_state(Book.book_name)
    await callback.message.answer("отличный выбор! выберите специалиста",reply_markup=kb.main_name)


@my_router.callback_query(F.data == "back",Book.book_name)
async def back_command(callback:CallbackQuery):
    await callback.message.edit_text("отлична! выберите улсугу которую хотите забранировать!",reply_markup=kb.main_inlne)
     

@my_router.callback_query(F.data == "strijka")
async def manikur(callback: CallbackQuery,state:FSMContext):
    await state.set_state(Book.book_strijka)
    await state.update_data(book_type="стрижка")
    await state.set_state(Book.book_name)
    await callback.message.answer("отличный выбор! выберите специалиста",reply_markup=kb.main_name)


@my_router.callback_query(F.data == "back",Book.book_name)
async def back_command(callback:CallbackQuery):
    await callback.message.edit_text("отлична! выберите улсугу которую хотите забранировать!",reply_markup=kb.main_inlne)
     
@my_router.message(F.text.in_(["13:30", "14:30", "18:30"]))
async def handle_finish(message:Message,state:FSMContext):
    await state.update_data(book_data = message.text)
    data = await state.get_data()

    user_id = message.from_user.id
    service_type = data.get("book_type")
    name_specialist = data.get("book_name")
    data_book = data.get("book_data")
    
    async with aiosqlite.connect("menegers_Books.db") as db:
        cursor = await db.execute(
            "SELECT 1 FROM Books WHERE name_specialist = ? AND data_book = ?",
            (name_specialist, data_book)
        )
        if await cursor.fetchone():
            await message.answer("Это время уже занято 😕. Пожалуйста, выберите другое.")
            return
        
        await password_sql(
        user_id=user_id,
        service_type=service_type,
        name_specialist=name_specialist,
        data_book=data_book)

    await message.answer(
        f"Вы успешно выбрали услугу.\n"
        f"Специалист: {data.get('book_name')}\n"
        f"Время: {data.get('book_data')}\n"
        f"Ждём вас у нас! 😊",reply_markup=kb.main_keyboard)
    await state.clear()


@my_router.message(F.text == "мои забранированые услуги")
async def watch_books_command(message: Message):
    credentials = await get_all_credentials(message.from_user.id)
    if not credentials:
        await message.answer("У вас пока нет забронированных услуг.")
        return
    
    text = "\n".join([f"• {z}" for z in credentials])
    await message.answer(f"Вот ваши забронированные услуги:\n{text}")

async def get_all_credentials(user_id: int):

    async with aiosqlite.connect("menegers_Books.db") as db:
        async with db.execute("SELECT service_type, name_specialist, data_book FROM Books WHERE user_id = ?", (user_id,)) as cursor:
            rows = await cursor.fetchall()
            return [f"{row[0]} — {row[1]} — {row[2]}" for row in rows]
