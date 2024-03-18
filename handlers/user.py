from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from contextlib import suppress
import string_const
import config
import asyncio
import datetime
from founder import database, bot
import keyboards
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton  #ReplyKeyboardRemove
from aiogram.utils.exceptions import (MessageToEditNotFound, MessageCantBeEdited, MessageCantBeDeleted, MessageToDeleteNotFound)
from aiogram.utils.deep_linking import get_start_link, decode_payload
import time

async def delete_message(message: types.Message, sleep_time: int = 0):
    await asyncio.sleep(sleep_time)
    with suppress(MessageToEditNotFound, MessageCantBeEdited, MessageCantBeDeleted, MessageToDeleteNotFound):
        await message.delete()

async def start(message: types.Message, state: FSMContext): 
  if message.chat.type == 'private':
    if not database.user_exist(message.from_user.id):
      await message.answer(string_const.START_TEXT, disable_web_page_preview=True,
                           reply_markup=keyboards.main_kb)
      # referral system
      args = message.get_args()
      referral_id = decode_payload(args)
      if referral_id != '': 
        if referral_id != str(message.from_user.id):
          try:
            database.add_referral(referral_id)
            await bot.send_message(referral_id, string_const.YOUR_REFERRAL_REGISTERED_TEXT)
            await bot.send_message(config.MODERATION_CHAT_ID, string_const.NEW_REFERRAL_USER_TEMPLATE.safe_substitute(user_id = message.from_user.id, referral_id = referral_id))
            
          except:
            pass
        else:
          await message.answer(string_const.NOT_REGISTER_WITH_YOUR_LINK_TEXT)
      #
      database.add_user(message.from_user.id, message.from_user.username,
                        ".".join(str(datetime.datetime.now()).split('.')[:-1]),
                        message.from_user.first_name,
                        message.from_user.last_name, referral_id)

    else:
      current_state = await state.get_state()
      if current_state:
        await state.finish()
      chat = database.get_chat(message.from_user.id)
      if chat:
        await message.answer(string_const.YOU_DISCONNECTED_TEXT,
                             reply_markup=keyboards.main_kb)
        await bot.send_message(chat[1],
                               string_const.PARTNER_DISCONNECTED_TEXT,
                               reply_markup=keyboards.main_kb)
        msg =  await bot.send_message(chat[1],string_const.LEAVE_OPINION_TEXT,reply_markup=keyboards.after_dialogue_kb)
        asyncio.create_task(delete_message(msg, config.OPINION_TIME))
        database.delete_chat(message.from_user.id)
        
      database.delete_queue(message.from_user.id)

    database.update_user(message.from_user.id, message.from_user.username, message.from_user.first_name, message.from_user.last_name)
    await message.answer(string_const.START_COMMAND_TEXT,
                         reply_markup=keyboards.main_kb)

  else:
    await message.answer("Bot work only in private chat!")


async def start_search(message: types.Message):
  if database.get_status(message.from_user.id) == "MUT":
    await message.answer(string_const.MUT_TEXT)
    return
    
  partner = database.get_queue()
  if database.create_chat(message.from_user.id, partner) is False:
    database.add_queue(message.from_user.id)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton(string_const.STOP_SEARCH_BTN_TEXT)
    markup.add(btn)

    await message.answer(string_const.SEARCH_PARTNER_TEXT, reply_markup=markup)

  else:
    database.delete_queue(message.from_user.id)
    database.delete_queue(partner)

    # database.set_user_history(message.from_user.id, partner)
    # database.set_user_history(partner, message.from_user.id)
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton(string_const.DISCONNECT_BTN_TEXT)
    markup.add(btn)

    await message.answer(string_const.CONNECTED_TEXT, reply_markup=markup)
    await bot.send_message(partner,
                           string_const.CONNECTED_TEXT,
                           reply_markup=markup)
    

async def disconnect(message: types.Message):
  chat = database.get_chat(message.from_user.id)
  if chat:
    #  
    partner = database.get_chat(message.from_user.id)[1]
    database.set_user_history(message.from_user.id, partner)
    database.set_user_history(partner, message.from_user.id)
    # 
    await message.answer(string_const.YOU_DISCONNECTED_TEXT,
                         reply_markup=keyboards.main_kb)
    await bot.send_message(chat[1],
                           string_const.PARTNER_DISCONNECTED_TEXT,
                           reply_markup=keyboards.main_kb)
    msg = await message.answer(string_const.LEAVE_OPINION_TEXT,reply_markup=keyboards.after_dialogue_kb)
    asyncio.create_task(delete_message(msg, config.OPINION_TIME))
    msg =  await bot.send_message(chat[1],string_const.LEAVE_OPINION_TEXT,reply_markup=keyboards.after_dialogue_kb)
    asyncio.create_task(delete_message(msg, config.OPINION_TIME))
    database.delete_chat(message.from_user.id)
  else:
    await message.answer(string_const.YOU_NOT_CONNECTED_TEXT,
                         reply_markup=keyboards.main_kb)


async def stop_search(message: types.Message):
  database.delete_queue(message.from_user.id)
  await message.answer(string_const.SEARCH_STOPED, reply_markup=keyboards.main_kb)


###########################################################################
async def help(message: types.Message):
  await message.answer(string_const.HELP_TEXT)


async def vip(message: types.Message):
  pass


async def about_bot(message: types.Message):
  await message.answer(string_const.ABOUT_BOT_TEXT)
  

async def referral_system(message: types.Message):
  ref_link = await get_start_link(str(message.from_user.id), encode=True)
  await message.answer(string_const.REFERRAL_PROGRAM_TEMPLATE.safe_substitute(ref_link = ref_link))
  

async def profile(message: types.Message):
  rating_list = database.get_rating_list()
  referral_list = database.get_referral_list()
    
  rating = database.get_rating(message.from_user.id)[0]
  rating_place = sorted(list(set(rating_list)))[::-1].index(rating) + 1
  referral = database.get_referral(message.from_user.id)[0]
  referral_place = sorted(list(set(referral_list)))[::-1].index(referral) + 1

  status = database.get_status(message.from_user.id)
  if status == "FREE":
    status_description = ""
  elif status == "MUT":
    mut_time = (database.get_mut_time(message.from_user.id) - int(time.time()))//3600 + 1
    if mut_time == 1:
      status_description = f"ещё {mut_time} час"
    else:
      status_description = f"ещё {mut_time} часов"
  await message.answer(string_const.PROFILE_TEMPLATE.safe_substitute(status = status, status_description = status_description, rating = rating, rating_place = rating_place, referral = referral, referral_place = referral_place))


async def support(message: types.Message):
  await message.answer(string_const.SUPPORT_TEXT)
  await bot.send_message(config.MODERATION_CHAT_ID, string_const.POTENTIAL_SPONSOR_TEMPLATE.safe_substitute(user_id = message.from_user.id))


###########################################################################
# @dispatcher.message_handler(content_types=types.ContentTypes.TEXT)
async def text_handler(message: types.Message):
  chat = database.get_chat(message.chat.id)
  await bot.send_message(chat[1], message.text)


# @dispatcher.message_handler(content_types=types.ContentTypes.VOICE)
async def voice_handler(message: types.Message):
  chat = database.get_chat(message.chat.id)

  if chat:
    await bot.send_voice(chat[1], message.voice.file_id)


# @dispatcher.message_handler(content_types=types.ContentTypes.PHOTO)
async def photo_handler(message: types.Message):
  chat = database.get_chat(message.chat.id)

  if chat:
    await bot.send_photo(chat[1], message.photo[-1].file_id)


# @dispatcher.message_handler(content_types=types.ContentTypes.DOCUMENT)
async def doc_handler(message: types.Message):
  chat = database.get_chat(message.chat.id)

  if chat:
    await bot.send_document(chat[1], message.document.file_id)


# @dispatcher.message_handler(content_types=types.ContentTypes.VIDEO)
async def video_handler(message: types.Message):
  chat = database.get_chat(message.chat.id)

  if chat:
    await bot.send_video(chat[1], message.video.file_id)


# @dispatcher.message_handler(content_types=types.ContentTypes.STICKER)
async def stick_handler(message: types.Message):
  chat = database.get_chat(message.chat.id)

  if chat:
    await bot.send_sticker(chat[1], message.sticker.file_id)


# @dispatcher.message_handler(content_types=types.ContentTypes.AUDIO)
async def audio_handler(message: types.Message):
  chat = database.get_chat(message.chat.id)

  if chat:
    await bot.send_audio(chat[1], message.audio.file_id)


# @dispatcher.message_handler(content_types=types.ContentTypes.VIDEO_NOTE)
async def video_note_handler(message: types.Message):
  chat = database.get_chat(message.chat.id)

  if chat:
    await bot.send_video_note(chat[1], message.video_note.file_id)


def register_handlers_user(dispathcer: Dispatcher):
  dispathcer.register_message_handler(start, commands=['start'], state="*")
  
  dispathcer.register_message_handler(
    start_search,
    Text(equals=string_const.START_SEARCH_BTN_TEXT),
    lambda message: message.chat.type == 'private',
    lambda message: database.get_chat(message.from_user.id) == False, 
    content_types=["text"])

  dispathcer.register_message_handler(
    disconnect,
    Text(equals=string_const.DISCONNECT_BTN_TEXT),
    lambda message: message.chat.type == 'private',
    content_types=["text"])#lambda message: database.get_chat(message.from_user.id) != False,

  dispathcer.register_message_handler(
    stop_search,
    Text(equals=string_const.STOP_SEARCH_BTN_TEXT),
    lambda message: message.chat.type == 'private',
    lambda message: database.get_chat(message.from_user.id) == False,
    content_types=["text"])

  dispathcer.register_message_handler(
    vip,
    Text(equals=string_const.VIP_BTN_TEXT),
    lambda message: message.chat.type == 'private',
    lambda message: database.get_chat(message.from_user.id) == False,
    content_types=["text"])

  dispathcer.register_message_handler(
    help,
    Text(equals=string_const.HELP_BTN_TEXT),
    lambda message: message.chat.type == 'private',
    lambda message: database.get_chat(message.from_user.id) == False,
    content_types=["text"])

  dispathcer.register_message_handler(
    referral_system,
    Text(equals=string_const.REFERRAL_PROGRAM_BTN_TEXT),
    lambda message: message.chat.type == 'private',
    lambda message: database.get_chat(message.from_user.id) == False,
    content_types=["text"])

  dispathcer.register_message_handler(
    about_bot,
    Text(equals=string_const.ABOUT_BOT_BTN_TEXT),
    lambda message: message.chat.type == 'private',
    lambda message: database.get_chat(message.from_user.id) == False,
    content_types=["text"])

  dispathcer.register_message_handler(
    profile,
    Text(equals=string_const.PROFILE_BTN_TEXT),
    lambda message: message.chat.type == 'private',
    lambda message: database.get_chat(message.from_user.id) == False,
    content_types=["text"])

  dispathcer.register_message_handler(
    support,
    Text(equals=string_const.SUPPORT_BTN_TEXT),
    lambda message: message.chat.type == 'private',
    lambda message: database.get_chat(message.from_user.id) == False,
    content_types=["text"])

  ###lambda message: database.get_chat(message.from_user.id) != False,
  dispathcer.register_message_handler(
    text_handler,
    lambda message: database.get_chat(message.from_user.id) != False,
    content_types=types.ContentTypes.TEXT,
  )
  dispathcer.register_message_handler(
    voice_handler,
    lambda message: database.get_chat(message.from_user.id) != False,
    content_types=types.ContentTypes.VOICE)
  dispathcer.register_message_handler(
    photo_handler,
    lambda message: database.get_chat(message.from_user.id) != False,
    content_types=types.ContentTypes.PHOTO)
  dispathcer.register_message_handler(
    doc_handler,
    lambda message: database.get_chat(message.from_user.id) != False,
    content_types=types.ContentTypes.DOCUMENT)
  dispathcer.register_message_handler(
    video_handler,
    lambda message: database.get_chat(message.from_user.id) != False,
    content_types=types.ContentTypes.VIDEO)
  dispathcer.register_message_handler(
    stick_handler,
    lambda message: database.get_chat(message.from_user.id) != False,
    content_types=types.ContentTypes.STICKER)
  dispathcer.register_message_handler(
    audio_handler,
    lambda message: database.get_chat(message.from_user.id) != False,
    content_types=types.ContentTypes.AUDIO)
  dispathcer.register_message_handler(
    lambda message: database.get_chat(message.from_user.id) != False,
    video_note_handler,
    content_types=types.ContentTypes.VIDEO_NOTE)
