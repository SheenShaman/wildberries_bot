from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart

from app.database.database import SessionLocal
from app.database.models import History
from app.keyboards import main, inline_keyboard
from app.product_info import get_product_info

from main import bot

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
async def get_info_database(message: Message):
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
async def stop_notification(message: Message):
    u_id = message.from_user.id
    user_history = session.query(History).filter(History.user_id == u_id).order_by(History.query_time.desc()).first()
    if user_history and user_history.subscribed is True:
        user_history.subscribed = False
        session.commit()
        await message.answer(
            text="Вы отписаны от уведомлений.",
            reply_markup=inline_keyboard().as_markup()
        )
    else:
        await message.answer(
            text="Вы не подписаны на уведомления.",
            reply_markup=inline_keyboard().as_markup()
        )


@router.callback_query(F.data == "subscribe")
async def send_notification(callback: CallbackQuery):
    u_id = callback.from_user.id
    user_history = session.query(History).filter(History.user_id == u_id).order_by(History.query_time.desc()).first()
    if user_history and user_history.subscribed is False:
        article = user_history.article
        user_history.subscribed = True
        session.commit()
        session.close()
        response = get_product_info(article)
        product_info = ",\n".join([f'{key} - {value}' for key, value in response.items()])
        await bot.send_message(u_id, product_info)
        await callback.message.answer("Вы подписаны на уведомления.")
    elif user_history is None:
        await callback.message.answer(
            text="Вашей истории запросов еще нет в базе. Начните получать информацию по товарам.",
            reply_markup=inline_keyboard().as_markup()
        )
    else:
        await callback.message.answer(
            text="Вы уже подписаны на уведомления.",
            reply_markup=inline_keyboard().as_markup()
        )
