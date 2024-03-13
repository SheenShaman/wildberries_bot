from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Получить информацию по товару')],
    [KeyboardButton(text='Остановить уведомления')],
    [KeyboardButton(text='Получить информацию из БД')],
], resize_keyboard=True, input_field_placeholder='Выберите пункт меню ниже')


def inline_keyboard():
    kb_builder = InlineKeyboardBuilder()
    kb_builder.add(InlineKeyboardButton(
        text="подписаться", callback_data="subscribe")
    )
    return kb_builder
