from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from aiogram.filters import CommandStart

from app.database.database import SessionLocal
from app.database.models import History
from app.keyboards import main, inline_keyboard
from app.product_info import get_product_info

session = SessionLocal()

router = Router()


class Article(StatesGroup):
    numbers = State()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await message.answer(
        text=f'Привет, {message.from_user.first_name}!\n'
             f'Выберите пункт(кнопку) меню ниже',
        reply_markup=main
    )
    await state.set_state(Article.numbers)


@router.message(F.text == "Получить информацию по товару")
async def input_article(message: Message, state: FSMContext):
    await message.answer(
        text='Введите артикул товара',
        reply_markup=inline_keyboard().as_markup()
    )
    await state.set_state(Article.numbers)


@router.message(Article.numbers)
async def get_product(message: Message, state: FSMContext):
    article = message.text.lower()
    product_response = get_product_info(article)
    if product_response == "Неверный артикул":
        await message.answer(
            text='Вы ввели неверный артикул товара.\nВведите артикул еще раз',
            reply_markup=inline_keyboard().as_markup()
        )
        await state.set_state(Article.numbers)
    else:
        session.add(
            History(
                user_id=message.from_user.id,
                article=article
            )
        )
        session.commit()

        product_info = ",\n".join([f'{key} - {value}' for key, value in product_response.items()])
        await message.answer(
            text=product_info,
            reply_markup=inline_keyboard().as_markup()
        )


@router.message(F.text == "Получить информацию из БД")
async def get_info_database(message: Message, state: FSMContext):
    last_info = session.query(History).all()[-5:]
    if last_info:
        for query in last_info:
            query_time = query.query_time.strftime("%d.%m.%Y %H:%M")
            await message.answer(
                text=(
                    f"id Пользователя - {query.user_id}\n"
                    f"Время запроса - {query_time}\n"
                    f"Артикул товара - {query.article}\n"
                ),
                reply_markup=inline_keyboard().as_markup()
            )
    else:
        await message.answer(
            text="Отсуствуют данные.",
            reply_markup=inline_keyboard().as_markup()
        )


@router.message(F.text == "Остановить уведомления")
async def stop_notification(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_history = session.query(History).filter(History.user_id == user_id).order_by(History.query_time.desc()).first
    if user_history and user_history.subscribe is True:
        user_history.subscribe = False
        session.commit()
        await message.answer(
            text="Вы отписаны от уведомлений.",
            reply_markup=inline_keyboard().as_markup()
        )
    else:
        await message.message.answer(
            text="Вы не подписаны на уведомления.",
            reply_markup=inline_keyboard().as_markup()
        )
