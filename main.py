import asyncio
import config
import Keyboards as kb
import db
import Buttons as bu
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.middlewares.logging import LoggingMiddleware
loop = asyncio.get_event_loop()

bot = Bot(token=config.TOKEN, loop=loop, parse_mode="HTML")
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

class name(StatesGroup):
    name = State()
    text = ''
class postindex(StatesGroup):
    postindex = State()
    text = ''
class address(StatesGroup):
    address = State()
    text = ''
def cart_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.InlineKeyboardButton(text=name, callback_data=cb) for name, cb in
                  {'Оформить заказ': 'ORD'}.items()])
    keyboard.add(*[types.InlineKeyboardButton(text=name, callback_data=cb) for name, cb in
                   {'Назад - ⬅️': 'BACK'}.items()])
    return keyboard


def getPriceCount(tid):
    cart = db.getcart(tid)
    count = len(cart)
    if count == 0:
        pass
    else:
        element = 0
        totalprice = 0
        while element < count:
            item = db.getItemByID(cart[element][4])
            totalprice = totalprice + (cart[element][2] * cart[element][3])
            element = element + 1
        return totalprice

def welcome_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.InlineKeyboardButton(text=name, callback_data=cb) for name, cb in
                   {'Каталог': 'T'}.items()])
    keyboard.add(*[types.InlineKeyboardButton(text=name, callback_data=cb) for name, cb in
                   {'Корзина': 'C'}.items()])
    return keyboard

@dp.message_handler(commands=['start'])
async def process_start_command(m: types.Message):
    await bot.send_message(m.chat.id, "Для просмотра каталога нажмите кнопку ниже", reply_markup=welcome_keyboard())


@dp.message_handler(state=name.name)
async def input_report(m: types.Message, state: FSMContext):
    db.addfio(m.text, m.chat.id)
    await bot.send_message(m.chat.id,f'Введите почтовый индекс')
    await postindex.first()
@dp.message_handler(state=postindex.postindex)
async def input_report(m: types.Message, state: FSMContext):
    db.addpost(m.text, m.chat.id)
    await bot.send_message(m.chat.id,f'Введите адрес (Город/Улица/Дом/Корпус/Квартира)')
    await address.first()
@dp.message_handler(state=address.address)
async def input_report(m: types.Message, state: FSMContext):
    db.addaddress(m.text, m.chat.id)
    ord = db.getusers(m.chat.id)
    print(f'ord 1{ord[0][3]}')
    cart = db.getcart(m.chat.id)
    count = len(cart)
    element = 0
    totalprice = 0
    itm = ''
    while element < count:
            item = db.getItemByID(cart[element][4])
            totalprice = totalprice + (cart[element][2] * cart[element][3])
            itm = itm + f'id {cart[element][4]} - {cart[element][2]} шт \n'
            element = element + 1
    db.addorder(ord[0][3],ord[0][4],itm,totalprice,ord[0][2])
    await bot.send_message(m.chat.id,f'Заказ оформлен, с вами свяжется администратор для оплаты.')
    db.finalcart(m.chat.id)
    db.finalusers(m.chat.id)
    await state.finish()
@dp.callback_query_handler(text_contains='addcart_')
async def addcartqu(call: types.CallbackQuery):
    if call.data and call.data.startswith("addcart_"):
        pos = call.data
        code = pos[pos.find('_')+1:]
        if code.isdigit():
            code = int(code)
            kb = bu.StoreKb(int(code))
            item = db.getItemByID(code)
            print(item)
            db.addItemToCart(call.from_user.id,item[0][0],1,item[0][1])
            await bot.answer_callback_query(callback_query_id=call.id,text="Добавлено в корзину",show_alert=True)
            print(f' Добавлено в корзину {call.from_user.id} : {item[0][0]} {1} {item[0][1]}')
            await call.message.edit_reply_markup(kb)
        else:
            await bot.answer_callback_query(call.id)

@dp.callback_query_handler(text_contains='c_')
async def addcartqu(call: types.CallbackQuery):
    if call.data and call.data.startswith("c_+"):
        print(call.from_user.id)
        pos = call.data
        code = pos[pos.find('+_') + 2:]
        print(f'code {code}')
        db.updCountCart(call.from_user.id,code)
        item = db.getItemByID(code)
        cart = db.getcartID(call.from_user.id,code)
        kb = bu.createCartKb(cart[0][4])
        totalprice = getPriceCount(call.from_user.id)
        await call.message.edit_text(f'{item[0][3]}  Цена: {cart[0][3]} ₽ \nКоличество: {cart[0][2]}\nОбщая цена за позицию: {cart[0][2] * cart[0][3]} ₽\n Цена заказа после изменения: {totalprice} ₽',reply_markup=kb)
    if call.data and call.data.startswith("c_-"):
        pos = call.data
        code = pos[pos.find('-_') + 2:]
        cart = db.getcartID(call.from_user.id, code)
        if cart[0][2] != 1:
            db.subCountCart(call.from_user.id, code)
            cart = db.getcartID(call.from_user.id, code)
            item = db.getItemByID(code)
            kb = bu.createCartKb(cart[0][4])
            totalprice = getPriceCount(call.from_user.id)
        await call.message.edit_text(f'{item[0][3]}  Цена: {cart[0][3]} ₽ \nКоличество: {cart[0][2]}\nОбщая цена за позицию: {cart[0][2] * cart[0][3]} ₽\n Цена заказа после изменения: {totalprice} ₽', reply_markup=kb)
    if call.data and call.data.startswith("c_delete"):
        pos = call.data
        code = pos[pos.find('e_') + 2:]
        db.delcartID(call.from_user.id,code)
        await call.message.edit_text('Позиция удалена')
@dp.callback_query_handler(text_contains='st_')
async def stob(call: types.CallbackQuery):
    if call.data and call.data.startswith("st_cart"):
        cart = db.getcart(call.from_user.id)
        count = len(cart)
        if count == 0:
            await bot.send_message(call.from_user.id, 'Ваша корзина пуста', reply_markup=welcome_keyboard())
        else:
            element = 0
            totalprice = 0
            while element < count:
                item = db.getItemByID(cart[element][4])
                kb = bu.createCartKb(cart[element][4])
                totalprice = totalprice + (cart[element][2] * cart[element][3])
                await bot.send_message(call.from_user.id,
                                       f'{item[0][3]}  Цена: {cart[element][3]} ₽ \n Количество : {cart[element][2]}\nОбщая цена за позицию {cart[element][2] * cart[element][3]} ₽',
                                       reply_markup=kb)
                element = element + 1
            await bot.send_message(call.from_user.id,
                                   f'Стоимость заказа: {totalprice} ₽\nПерейти к оформлению?',
                                   reply_markup=cart_keyboard())
    elif call.data and call.data.startswith("st_buy"):
        await bot.send_message(call.from_user.id, 'Введите имя для оформления заказа')
        await name.first()

    elif call.data and call.data.startswith("st_delete_"):
        pos = call.data
        code = pos[pos.find('e_') + 2:]
        db.delcartID(call.from_user.id, code)
        kb = bu.createInlineKb(code)
        await call.message.edit_reply_markup(kb)
    else:
        await bot.answer_callback_query(call.id)


@dp.message_handler(content_types='text', state="*")
async def echo_message(m: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    if m.text == 'Каталог':
        item = db.getItem()
        count = len(item)
        element = 0
        while element < count:
            kb = bu.createInlineKb(item[element][0])
            if item[element][4] == None:
                await bot.send_message(m.chat.id, f'{item[element][3]} — {item[element][1]} ₽', reply_markup=kb)
            else:
                await bot.send_photo(m.chat.id,photo=item[element][4],caption= f'{item[element][3]} — {item[element][1]} ₽', reply_markup=kb)
            element = element + 1
    elif m.text == 'Корзина':
        cart = db.getcart(m.chat.id)
        print(f'cart\n{cart}')
        count = len(cart)
        print(count)
        if count == 0:
            await bot.send_message(m.chat.id, 'Ваша корзина пуста', reply_markup=welcome_keyboard())
        else:
            element = 0
            totalprice=0
            while element < count:
                item = db.getItemByID(cart[element][4])
                print(item)
                kb = bu.createCartKb(cart[element][4])
                totalprice = totalprice + cart[element][2] * cart[element][3]
                await bot.send_message(m.chat.id, f'{item[0][3]}  Цена: {cart[element][3]} ₽ \n Количество : {cart[element][2]}\nОбщая цена за позицию {cart[element][2] * cart[element][3]} ₽',reply_markup=kb)
                element = element + 1
            await bot.send_message(m.chat.id, f'Стоимость заказа: {totalprice}\nПерейти к оформлению?',reply_markup=cart_keyboard())

    elif m.text == 'Оформить заказ':
        db.addUser(m.chat.id)
        await bot.send_message(m.chat.id,f'Введите ФИО на которое будет оформить заказ')
        await name.first()
    elif m.text == 'Назад - ⬅️':
        await bot.send_message(m.chat.id, 'Вы в главном меню ', reply_markup=welcome_keyboard())


if __name__ == '__main__':
    print("PEBot")
    executor.start_polling(dp, skip_updates=True)
