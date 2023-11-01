import os

from aiogram.utils import executor
import random
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import Message, ContentType

# Replace 'YOUR_BOT_TOKEN' with your actual Telegram Bot API token
BOT_TOKEN = "6360625136:AAE_hTqBIl0CsJgeXM_qeCQHIo1KPGX-IHI"
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Replace 'stored_messages' with your own storage mechanism (e.g., database or list)
stored_messages = []


@dp.message_handler(commands=['start', ])
async def send_welcome(message: Message):
    await message.reply("Hello! I am your shuffle bot. Send me some messages or files then do /shuffle, and I'll shuffle them for you.")
    print(f"{message.from_user.full_name} is playing this bot")


@dp.message_handler(commands=['help', ])
async def send_welcome(message: Message):
    await message.reply("/start - play with bot \n\
/help - get a help (what commands are available)\n\
/shuffle - shuffle musics that have recently sent")
    print(f"{message.from_user.full_name} is playing this bot")
    

@dp.message_handler(commands=['shuffle'])
async def shuffle_music_files(message: Message):
    if len(stored_messages) > 1:
        random.shuffle(stored_messages)
        await send_shuffled_music_files(message.from_user.id)
    else:
        await message.reply("Please send more than one music file to shuffle.")


@dp.message_handler(content_types=ContentType.AUDIO)
async def save_music_file(message: Message):
    stored_messages.append(message.audio.file_id)
    await message.reply(f"Music file '{message.audio.title}' saved.")
    print(f"Music file '{message.audio.title}' saved.")


async def send_shuffled_music_files(user_id):
    random.shuffle(stored_messages)
    for file_id in stored_messages:
        await bot.send_audio(user_id, audio=file_id)
    await bot.send_message(user_id, "Here are your shuffled music files!")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
