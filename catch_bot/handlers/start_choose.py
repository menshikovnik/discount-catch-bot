import asyncio
import pyshorteners
from aiogram import Router, F, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters.state import State
from aiogram.filters.state import StatesGroup
from aiogram.fsm.context import FSMContext
from selenium.common import NoSuchElementException
from scripts import price_parser
from catch_bot.keyboards.for_start import get_choose_kb
from catch_bot.bot import bot
from aiogram.utils.markdown import hide_link
from database import database
from aiogram import html

router = Router()


class AddProduct(StatesGroup):
    product_vc = State()


@router.message(Command("start"))  # [2]
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    username = html.bold(html.quote(message.from_user.username))
    if username is None:
        await message.answer("Для продолжения укажите имя пользователя в настройках Telegram")
    else:
        await message.answer(f"Hello, {username} это бот "
                             f"для ловли скидок на маркетплейсе Ozon\n\n"
                             "<b>Выберите одну из команд</b>\n\n"
                             "/menu - Меню\n"
                             "/help - Помощь",
                             parse_mode=ParseMode.HTML, reply_markup=types.ReplyKeyboardRemove())


@router.message(Command("menu"))
async def start_menu(message: Message):
    await message.answer("Что вы хотите сделать?", reply_markup=get_choose_kb())
    await message.delete()


@router.message(F.text.lower() == "добавить товар")
async def input_vc(message: types.Message, state: FSMContext):
    await message.answer("Введите артикул", reply_markup=None)
    await state.set_state(AddProduct.product_vc)


@router.message(F.text.lower() == "отмена")
async def cancel(message: types.Message):
    msg = await message.answer("Возврат к меню...", reply_markup=ReplyKeyboardRemove())
    await message.delete()
    await asyncio.sleep(2)
    await bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)


@router.message(AddProduct.product_vc)
async def add_product(message: types.Message, state: FSMContext):
    vc = message.text
    msg = await message.answer("Загрузка...")
    s = pyshorteners.Shortener()
    try:
        price = price_parser.price_parse(vc)
        url = s.tinyurl.short(price_parser.get_cur_url().strip())
        username = message.from_user.username
        database.add_product(username, vc, price)
        await message.reply(f"Товар по артикулу {vc} успешно добавлен!\n\n"
                            f"Цена данного товара: {price}" + "р\n" +
                            hide_link(url),
                            parse_mode=ParseMode.HTML)
        await bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)
    except NoSuchElementException:
        await bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)
        await msg.answer("Введен неверный артикул, попробуйте еще раз")
    await state.clear()

    @router.shutdown
    async def on_shutdown():
        database.close_connection()
