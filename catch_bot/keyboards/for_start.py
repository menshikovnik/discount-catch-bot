from aiogram.types import ReplyKeyboardMarkup
from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_choose_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(types.KeyboardButton(text="Добавить товар"),
                types.KeyboardButton(text="Мои товары"))
    builder.row(types.KeyboardButton(text="Отмена"))

    return builder.as_markup(one_time_keyboard=True, resize_keyboard=True,
                             input_field_placeholder="Выберите вариант")