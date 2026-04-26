from aiogram.types import Message,CallbackQuery
from aiogram.filters import Command
from aiogram import Router,F
import sys 
from hendller import keyboard as kb
import aiosqlite
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup,State
import os


admin_router = Router(name=__name__)


ADMIN_ID = int(os.getenv('ADMIN_ID'))
ADMIN_ID = ADMIN_ID


class Books(StatesGroup):
    id_enter = State()

@admin_router.message(Command("admin"))
async def admin_panel(message: Message):
    if message.from_user.id not in ADMIN_ID:
        return await message.answer("У вас нет доступа 🛑")
   
    await message.answer(f"добро пожаловать администритор {message.from_user.full_name}!",reply_markup=kb.admin_ponel)

@admin_router.callback_query(F.data == "admin_all")
async def admin_all(callback: CallbackQuery):
    async with aiosqlite.connect("menegers_Books.db") as db:
        async with db.execute("SELECT * FROM Books") as cursor:
            rows = await cursor.fetchall()

    if not rows:
        return await callback.message.answer("Бронирований пока нет.")

    text = "\n\n".join([
        f"👤 ID{r[0]}\n📅 {r[1]}\n{r[3]}"
        for r in rows
    ])
    await callback.message.answer(f"Все бронирования:\n{text}")

@admin_router.callback_query(F.data == "admin_delete_all")
async def admin_delete_all(callback: CallbackQuery):
    async with aiosqlite.connect("menegers_Books.db") as db:
        await db.execute("DELETE FROM Books")
        await db.commit()

    await callback.message.answer("Все брони успешно удалены ✅")

@admin_router.callback_query(F.data == "admin_stats")
async def admin_stats(callback: CallbackQuery):
    async with aiosqlite.connect("menegers_Books.db") as db:
        async with db.execute("SELECT COUNT(*) FROM Books") as cursor:
            count = (await cursor.fetchone())[0]

    await callback.message.answer(f"Всего бронирований: {count}")

@admin_router.callback_query(F.data=="admin_delate")
async def admin_delete(callback:CallbackQuery,state:FSMContext):
    await state.set_state(Books.id_enter)
    async with aiosqlite.connect("menegers_Books.db") as db:
        async with db.execute("SELECT * FROM Books") as cursor:
            rows = await cursor.fetchall()
        if rows == 0:
            await callback.message.answer("в ностаящий момент нету зарегестрированых сеансов подождите пока они появиться")
            return
        msg = "Список пользоватлей:\n"
        for row in rows:
            msg += f"ID: {row[0]}, Имя:{row[2]}, Сеанс:{row[1]}\n"   
        await callback.message.answer(f"{msg}\n\nВведите ID, который хотите удалить:")

@admin_router.message(Books.id_enter)
async def admin_delete_register(message:Message,state:FSMContext):
    try:
        delete_id = int(message.text)
    except ValueError:
        await message.answer("Пожалуйста, введите числовой ID.")
        return

    async with aiosqlite.connect("menegers_Books.db") as db:
        await db.execute("DELETE FROM Books WHERE user_id = ?", (delete_id,))
        await db.commit()

    await message.answer(f"Сеанс с ID {delete_id} был удалён.")
    await state.clear()
