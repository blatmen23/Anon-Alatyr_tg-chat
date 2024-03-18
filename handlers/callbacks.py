from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
import string_const
import config
import datetime 
from founder import database, bot
import keyboards
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton #ReplyKeyboardRemove


async def complain(callback: types.CallbackQuery):
    await callback.message.edit_text("Выберите причину:", reply_markup=keyboards.complain_kb)

async def like(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    partner_id = database.get_user_history(user_id)[2]

    if partner_id == database.get_user_history(user_id)[2]:
      await bot.send_message(config.MODERATION_CHAT_ID, string_const.SUSPECTS_RATING_CHEATING_TEMPLATE.safe_substitute(user_id = user_id, partner_id = partner_id))
    
    database.add_rating(partner_id)
    await callback.answer(text="Рейтинг собеседника повышен.", show_alert=True)
    await callback.message.delete()
  
async def dislike(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    partner_id = database.get_user_history(user_id)[2]
    
    if database.get_rating(partner_id)[0] > 0:
      database.minus_rating(partner_id, 1)
    await callback.answer(text="Рейтинг собеседника понижен.", show_alert=True)
    await callback.message.delete()

  
async def take_violation(callback: types.CallbackQuery):
    await callback.answer(text=string_const.COMPLAIN_CAUSE_SEND_ALERT_TEXT, show_alert=True)
    user_id = callback.from_user.id
    partner_id = database.get_user_history(user_id)[2]
  
    print("Жалоба от", user_id, "на", partner_id)
    database.add_complaint(partner_id)
    await bot.send_message(config.MODERATION_CHAT_ID, string_const.ADD_VIOLATION_TEMPLATE.safe_substitute(user_id = partner_id))
  
    if database.get_complaint(partner_id)[0] >= config.VIOLATIONS_COUNT_FOR_MUT:
      database.set_complaint(partner_id, 0)
      database.give_mut_status(partner_id, config.MUT_TIME)
      await bot.send_message(partner_id, string_const.MUT_TEXT, reply_markup=keyboards.main_kb)
      await bot.send_message(config.MODERATION_CHAT_ID, string_const.MUT_MODERATION_TEMPLATE.safe_substitute(user_id = partner_id, mut_time = config.MUT_TIME))
      print(f"Жалоба от {user_id} отправила {partner_id} в мут")
    await callback.message.delete()    

async def back(callback: types.CallbackQuery):
    await callback.message.edit_text(string_const.LEAVE_OPINION_TEXT, reply_markup=keyboards.after_dialogue_kb)


def register_handlers_callbacks(dispathcer: Dispatcher):
    dispathcer.register_callback_query_handler(complain, text = "complain")
    dispathcer.register_callback_query_handler(like, text = "like")
    dispathcer.register_callback_query_handler(dislike, text = "dislike")
    dispathcer.register_callback_query_handler(take_violation, text = ["threats", "advertising", "abuse", "materials18", "other"])
    dispathcer.register_callback_query_handler(back, text = "back")