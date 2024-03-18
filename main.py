from aiogram.utils import executor
from founder import database, dispatcher

from complaint_cleaner import complaint_cleaner
from keep_alive import keep_alive

from handlers import admin, user, callbacks

user.register_handlers_user(dispatcher)
admin.register_handlers_admin(dispatcher)
callbacks.register_handlers_callbacks(dispatcher)

complaint_cleaner()
keep_alive()

async def on_startup(_):
  print("anon chat bot...")
  database.clear_chats_table()
  print("`chats` table is clear")
  print("anon chat bot working")

if __name__ == '__main__':
    executor.start_polling(dispatcher, skip_updates=True, on_startup=on_startup)
