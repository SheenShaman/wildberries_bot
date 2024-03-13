from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from aiogram.filters import CommandStart

import app.keyboards as kb
from app.product_info import get_product_info

router = Router()


class Article(StatesGroup):
    numbers = State()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f'Привет, {message.from_user.first_name}!')


@router.message(F.text == "Получить информацию по товару")
async def input_article(message: Message, state: FSMContext):
    await message.answer('Введите артикул товара', reply_markup=kb.main)  # должна появиться кнопка Подписаться
    await state.set_state(Article.numbers)


@router.message(Article.numbers)
async def get_product(message: Message, state: FSMContext):
    article = message.text.lower()
    product_response = get_product_info(article)
    if product_response == "Неверный артикул":
        await message.answer('Вы ввели неверный артикул товара.\nВведите артикул еще раз')
        await state.set_state(Article.numbers)
    else:
        product_info = ",\n".join([f'{key} - {value}' for key, value in product_response.items()])
        await message.answer(text=product_info)

