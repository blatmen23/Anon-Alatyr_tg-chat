from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram import types
from founder import database, bot
from aiogram import Dispatcher
import config
import os
import asyncio
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton #ReplyKeyboardRemove
import keyboards
import string_const
import time

class FSMadmin(StatesGroup):
  image = State()
  text = State()
  link = State()
  confirmation = State()


# @dispatcher.message_handler(lambda message: message.from_user.id in config.ADMINS, commands=['sendall'])
async def sendall(message: types.Message):
    sender_kb = ReplyKeyboardMarkup(resize_keyboard = True)     
    sender_kb.add(KeyboardButton(text = "Выход"))
    await message.answer("Okey, send me a image", reply_markup = sender_kb)
    await FSMadmin.image.set()
  
  
# @dispatcher.message_handler(Text(equals='Выход'), state='*')
async def cancel_form(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await message.reply("Отмена", reply_markup=keyboards.main_kb)
        return
    await state.finish()
    await message.reply("Отмена", reply_markup=keyboards.main_kb)

# @dispatcher.message_handler(content_types=['photo'], state = FSMadmin.image)
async def take_image(message: types.message, state: FSMContext):
    async with state.proxy() as data:
      data['image'] = message.photo[-1].file_id
    await FSMadmin.next() 
    sender_kb = ReplyKeyboardMarkup(resize_keyboard = True)     
    sender_kb.add(KeyboardButton(text = "Выход"))
    await message.answer("Okey, send me a text", reply_markup = sender_kb) 
  
# @dispatcher.message_handler(content_types=['text'], state = FSMadmin.text)
async def take_text(message: types.message, state: FSMContext):
    async with state.proxy() as data:
      data['text'] = message.text
    await FSMadmin.next()
    sender_kb = ReplyKeyboardMarkup(resize_keyboard = True) 
    nolink_btn = KeyboardButton(text = "Без ссылки")
    exit_btn = KeyboardButton(text = "Выход")
    sender_kb.add(nolink_btn)
    sender_kb.add(exit_btn)
    await message.answer("Ссылка (если есть)", reply_markup = sender_kb)
  
# @dispatcher.message_handler(content_types=['text'], state = FSMadmin.link)
async def take_link(message: types.message, state: FSMContext):
    sender_kb = ReplyKeyboardMarkup(resize_keyboard = True)     
    sender_kb.add(KeyboardButton(text = "Выход"))
    if message.text != "Без ссылки":
      async with state.proxy() as data:
        data['link'] = message.text
    else:
      async with state.proxy() as data:
        data['link'] = "#"
    await FSMadmin.next() 
    await message.answer("Подтверждаем?", reply_markup = sender_kb)
    
    if data['link'] != "#" and (data['link'].startswith("https://") or data['link'].startswith("http://")):
      link_btn = InlineKeyboardButton(text = "👉 Перейти 👈", url = data['link'])
    else:
      link_btn = InlineKeyboardButton(text = "👉 Реклама 👈", url = string_const.ADVERTISING_CONTACT_LINK)

    confirm_btn = InlineKeyboardButton(text = "✅ Подтвердить", callback_data = "confirm")
    cancel_btn = InlineKeyboardButton(text = "❌ Отмена", callback_data = "cancel")
    
    link_kb = InlineKeyboardMarkup()
    link_kb.add(link_btn)
    link_kb.row(confirm_btn, cancel_btn)

    await bot.send_photo(chat_id=message.chat.id, photo=data['image'], caption=data['text'], reply_markup=link_kb)
  
    
async def take_confirmation(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
      pass
    users = database.get_users()
    await callback.message.answer("Okay let’s go!")
    
    if data['link'] != "#" and (data['link'].startswith("https://") or data['link'].startswith("http://")):
      link_btn = InlineKeyboardButton(text = "👉 Перейти 👈", url = data['link'])
    else:
      link_btn = InlineKeyboardButton(text = "👉 Реклама 👈", url = string_const.ADVERTISING_CONTACT_LINK)
    link_kb = InlineKeyboardMarkup()
    link_kb.add(link_btn)

    image = data['image']
    text = data['text']
    
    for row in users:
      try:
        await bot.send_photo(chat_id=row[1], photo=image, caption=text, reply_markup=link_kb)
        print(f"{row[0]} {row[1]} received ads")
        if int(row[2]) != 1:
          database.set_active(row[1], 1)
      except:
        database.set_active(row[1], 0)  
      await asyncio.sleep(config.TIME_BETWEEN_SENDLER_MESSAGE)

    await bot.send_message(callback.from_user.id, "Рассылка успешно завершена!")
    await state.finish()
    await callback.message.delete()    

async def help(message: types.message):
    await message.answer(string_const.ADMIN_HELP_TEXT)

async def take_cancel(callback: types.CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await bot.send_message(callback.from_user.id, "Отмена", reply_markup=keyboards.main_kb)
        return
    await state.finish()
    await bot.send_message(callback.from_user.id, "Отмена", reply_markup=keyboards.main_kb)
    await callback.message.delete()    

async def get_db_users(message: types.message):
    data_list = database.get_users()
    print(data_list)
    with open("logs/db_users.txt", "w", encoding="utf8") as file:
      for string in data_list:
        file.write(str(string) + "\n")
    await message.answer_document(open("logs/db_users.txt"))
    try:
      os.remove("logs/db_users.txt")
    except:
      pass
    
async def get_db_history(message: types.message):
    data_list = database.get_history()
    print(data_list)
    with open("logs/db_history.txt", "w", encoding="utf8") as file:
      for string in data_list:
        file.write(str(string) + "\n")
    await message.answer_document(open("logs/db_history.txt"))
    try:
      os.remove("logs/db_history.txt")
    except:
      pass

async def get_db_queue(message: types.message):
    data = database.get_queue_users()
    print(data)
    await message.answer(data)

async def set_status(message: types.message):
    status_arg = message.get_args()
    status_arg = status_arg.split(" ")
    try:
      if status_arg[1] == "FREE":
        database.give_free_status(status_arg[0])
        database.set_complaint(status_arg[0], 0)
        await bot.send_message(status_arg[0], string_const.PARDON_TEXT, reply_markup=keyboards.main_kb)
        await bot.send_message(config.MODERATION_CHAT_ID, string_const.FREE_MODERATION_TEMPLATE.safe_substitute(admin_id = message.from_user.id, user_id = status_arg[0]))
        await message.answer("Статус пользователя успешно изменён.")
      elif status_arg[1] == "MUT":
        database.set_complaint(status_arg[0], 0)
        database.give_mut_status(status_arg[0], int(status_arg[2]))
        await bot.send_message(status_arg[0], string_const.MUT_TEXT, reply_markup=keyboards.main_kb)
        await bot.send_message(config.MODERATION_CHAT_ID, string_const.MUT_MODERATION_TEMPLATE.safe_substitute(user_id = status_arg[0], mut_time = int(status_arg[2])))
        if int(status_arg[2]) == 1:
          print(f"Жалоба от {message.from_user.id} отправила {status_arg[0]} в мут на {int(status_arg[2])} час")
        else:
          print(f"Жалоба от {message.from_user.id} отправила {status_arg[0]} в мут на {int(status_arg[2])} часов")
        await message.answer("Статус пользователя успешно изменён.")
    except:
      await message.answer("Статус пользователя не изменён. Возможно, переданы неверные аргументы.")

async def minus_complaint(message: types.message):
    database.minus_complaint()

async def add_rating(message: types.message):
  if message.get_args() == "":
    return
  try:
    user_id = int(message.get_args())
    print(user_id)
    database.add_rating(user_id)
  except:
    pass
    
async def minuse_rating(message: types.message):
  if message.get_args() == "":
    return
  try:
    args = message.get_args()
    args = args.split(" ")
    user_id = int(args[0])
    quantity = int(args[1])
    
    print(user_id)
    database.minus_rating(user_id, quantity)
    await bot.send_message(user_id, string_const.DOWN_RATING_TEMPLATE.safe_substitute(quantity = quantity))
  except:
    pass

async def add_referral(message: types.message):
  if message.get_args() == "":
    return
  try:
      user_id = int(message.get_args())
      print(user_id)
      database.add_referral(user_id)
  except:
    pass

async def minus_referral(message: types.message):
  if message.get_args() == "":
    return
  try:
      user_id = int(message.get_args())
      print(user_id)
      database.minus_referral(user_id)
  except:
    pass

def register_handlers_admin(dispathcer: Dispatcher):
  dispathcer.register_message_handler(help, lambda message: message.from_user.id in config.ADMINS, commands=['help'])
  dispathcer.register_message_handler(sendall, lambda message: message.from_user.id in config.ADMINS, commands=['sendall'])
  dispathcer.register_message_handler(get_db_users, lambda message: message.from_user.id in config.ADMINS, commands=['get_db_users'])
  dispathcer.register_message_handler(get_db_history, lambda message: message.from_user.id in config.ADMINS, commands=['get_db_history'])
  dispathcer.register_message_handler(get_db_queue, lambda message: message.from_user.id in config.ADMINS, commands=['get_db_queue'])
  dispathcer.register_message_handler(set_status, lambda message: message.from_user.id in config.ADMINS, commands=['set_status'])
  dispathcer.register_message_handler(minus_complaint, lambda message: message.from_user.id in config.ADMINS, commands=['minus_complaint'])
  dispathcer.register_message_handler(add_rating, lambda message: message.from_user.id in config.ADMINS, commands=['add_rating'])
  dispathcer.register_message_handler(minuse_rating, lambda message: message.from_user.id in config.ADMINS, commands=['minus_rating'])
  dispathcer.register_message_handler(add_referral, lambda message: message.from_user.id in config.ADMINS, commands=['add_referral'])
  dispathcer.register_message_handler(minus_referral, lambda message: message.from_user.id in config.ADMINS, commands=['minus_referral'])
  
  dispathcer.register_message_handler(cancel_form, Text(equals='Выход'), state='*')
  dispathcer.register_message_handler(take_image, content_types=['photo'], state = FSMadmin.image)
  dispathcer.register_message_handler(take_text, content_types=['text'], state = FSMadmin.text)
  dispathcer.register_message_handler(take_link, content_types=['text'], state = FSMadmin.link)
  
  dispathcer.register_callback_query_handler(take_confirmation, text = "confirm", state = FSMadmin.confirmation)
  dispathcer.register_callback_query_handler(take_cancel, text = "cancel", state = FSMadmin.confirmation)
