from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,InlineKeyboardButton,InlineKeyboardMarkup

main_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="забранировать услугу!"),
                                               KeyboardButton(text="мои забранированые услуги")]])

main_inlne = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="маникуюр",callback_data="manikyur"),
                                                    InlineKeyboardButton(text="массаж",callback_data="massaj"),
                                                    InlineKeyboardButton(text="стрижка",callback_data="strijka")]])

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

main_name = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Егор", callback_data="Egoe"),
        InlineKeyboardButton(text="Гриша", callback_data="Grisha"),
        InlineKeyboardButton(text="Артём", callback_data="Artem")],
        [InlineKeyboardButton(text="без разницы", callback_data="bez_raznici")],
        [InlineKeyboardButton(text="назад", callback_data="back")]])

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_date = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="13:30")],
              [KeyboardButton(text="14:30")],
              [KeyboardButton(text="18:30")]],
    resize_keyboard=True,
    input_field_placeholder="выберите пункт меню..."
)

admin_ponel = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="все брони",callback_data="admin_all")],
                                                    [InlineKeyboardButton(text="удалить все",callback_data="admin_delete_all")],
                                                    [InlineKeyboardButton(text="Статистика", callback_data="admin_stats")],
                                                    [InlineKeyboardButton(text="удалить конкретную запис",callback_data="admin_delate")]])

