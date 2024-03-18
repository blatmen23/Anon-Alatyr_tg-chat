from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton #ReplyKeyboardRemove
import string_const
# 
# USER
# 
main_kb = ReplyKeyboardMarkup(resize_keyboard = True) 

search_btn = KeyboardButton(text = string_const.START_SEARCH_BTN_TEXT)
info_btn = KeyboardButton(text = string_const.ABOUT_BOT_BTN_TEXT)
rating_btn = KeyboardButton(text = string_const.PROFILE_BTN_TEXT)
support_btn = KeyboardButton(text = string_const.SUPPORT_BTN_TEXT)
vip_btn = KeyboardButton(text = string_const.VIP_BTN_TEXT)
help_btn = KeyboardButton(text = string_const.HELP_BTN_TEXT)
referral_system_btn = KeyboardButton(text = string_const.REFERRAL_PROGRAM_BTN_TEXT)

main_kb.add(search_btn)
main_kb.row(info_btn, rating_btn)
main_kb.add(referral_system_btn, support_btn)
#
complain_btn = InlineKeyboardButton(text = "✍️ Пожаловаться", callback_data = "complain")
like_btn = InlineKeyboardButton(text = "👍 Хорошо", callback_data = "like")
dislike_btn = InlineKeyboardButton(text = "👎 Плохо", callback_data = "dislike")

after_dialogue_kb = InlineKeyboardMarkup()
after_dialogue_kb.add(complain_btn)
after_dialogue_kb.row(like_btn, dislike_btn)
#
threats_btn = InlineKeyboardButton(text = "👊 Угрозы", callback_data = "threats")
advertising_btn = InlineKeyboardButton(text = "📢 Реклама", callback_data = "advertising")
abuse_btn = InlineKeyboardButton(text = "🤬 Оскорбления", callback_data = "abuse")
materials18_btn = InlineKeyboardButton(text = "🔞 Материалы 18+", callback_data = "materials18")
other_btn = InlineKeyboardButton(text = "⚠ Другое", callback_data = "other")
back_btn = InlineKeyboardButton(text = "🔙 Назад", callback_data = "back")

complain_kb = InlineKeyboardMarkup(row_width=1)

complain_kb.add(threats_btn, advertising_btn, abuse_btn, materials18_btn, other_btn, back_btn)