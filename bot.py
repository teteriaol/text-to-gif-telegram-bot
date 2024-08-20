import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command, CommandObject
from aiogram.types import FSInputFile
from main import text_to_gif
import os
import sys
from dotenv import load_dotenv
load_dotenv()


API_TOKEN = os.getenv('API_TOKEN')
if not API_TOKEN:
    logging.error("API_TOKEN not found")
    sys.exit(1)
    
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)

dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.reply("Hello there! I can convert your message to gif like this one:")
    input_file = FSInputFile('assets/example.gif')
    await message.answer_animation(input_file)


@dp.message(Command("about"))
async def cmd_about(message: types.Message):
    await message.reply("Available characters: 🇬🇧English letters, 🇺🇦Ukrainian letters, numbers, some special symbols.")


@dp.message(Command("convert"))
async def cmd_convert(message: types.Message, command: CommandObject):
    user_id = message.from_user.id
    input_text = command.args
    if input_text is None:
        await message.reply("Input can't be empty")
    elif len(input_text) < 40:
        await message.reply("Processing...")
        gif_path, unknown_symbols = text_to_gif('assets/yellow_rect.jpg', input_text, user_id)
        if unknown_symbols:
            await message.reply(f'Warning! Unknown symbols: {", ".join(set(unknown_symbols))}')
        try:
            input_file = FSInputFile(gif_path)
            await message.reply_animation(input_file)
        finally:
            os.remove(gif_path)
    else:
        await message.reply("Max. input string = 40")



async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
