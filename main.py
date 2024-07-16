import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

bot = Bot(token='7248202305:AAHejdkRwnKMYclyMIf--cR1YAUI5iyGgxg')
dp = Dispatcher()

kunlar_list = ['Dushanba', 'Seshanba',
            'Chorshanba', 'Payshanba',
            'Juma','Shanba']

kun_text=''

jadval = {}
for kun in kunlar_list:
    jadval[kun] = False

class Info(StatesGroup):
    info = State()

asosiy = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Dushanba'), KeyboardButton(text='Seshanba')],
    [KeyboardButton(text='Chorshanba'), KeyboardButton(text='Payshanba')],
    [KeyboardButton(text='Juma'), KeyboardButton(text='Shanba')]
])

edit_btn = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✏️O\'zgartirish', callback_data='edit')]
])

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer('🔽O\'zingizga kerakli bo\'limni tanlang:', reply_markup=asosiy)

@dp.message(F.text.in_({'Dushanba','Seshanba','Chorshanba','Payshanba','Juma','Shanba'}))
async def kunlar(message: Message):
    global jadval, kunlar_list, kun_text
    text = message.text
    jadval_get = jadval.get(text)
    if jadval_get == False:
        await message.answer('Ma\'lumot yo\'q🤷‍♂️', reply_markup=edit_btn)
        kun_text=text
    else:
        info_data = jadval.get(text)
        new_info = info_data.split(' ')
        edit_info = '\n▫️'.join(new_info)
        await message.answer(f'📆{text}\n\n▫️{edit_info}', reply_markup=edit_btn)
        kun_text=text

@dp.callback_query(F.data == 'edit')
async def inline_call(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Info.info)
    await callback.message.edit_text('🔽Ma\'lumotni huddi quyidagidek qilib yuboring:\n\nFanNomi-00:00 FanNomi-00:00 FanNomi-00:00')

@dp.message(Info.info)
async def get_info(message: Message, state: FSMContext):
    global jadval, kun_text
    await state.update_data(info=message.text)
    data = await state.get_data()
    jadval[kun_text]=data['info']
    await message.answer('Ma\'lumot o\'zgartirildi✅')
    info_data = jadval.get(kun_text)
    new_info = info_data.split(' ')
    edit_info = '\n▫️'.join(new_info)
    await message.answer(f'📆{kun_text}\n\n▫️{edit_info}', reply_markup=edit_btn)
    await state.clear()

@dp.message(F.text)
async def text_none(message:Message):
    await message.answer('Iltimos faqat sizga berilgan komandalardan bilan foydalaning❗️')

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
