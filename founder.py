from aiogram import Bot
from database import Database
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import config


database = Database()
storage = MemoryStorage()

bot = Bot(config.TOKEN,  parse_mode="HTML")
dispatcher = Dispatcher(bot, storage = storage)