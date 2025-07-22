import asyncio
import json
import os

from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv

from utils import encode_base64, decode_base64, store_access, get_user_lang
from i18n import _

load_dotenv()
bot = Bot(token=os.getenv("BOT_TOKEN"), parse_mode=ParseMode.HTML)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(msg: types.Message):
    lang = get_user_lang(msg.from_user.language_code)
    text = _(lang, "start")
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🇬🇧 English", callback_data="lang:en"),
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang:ru")
        ]
    ])
    await msg.answer(text, reply_markup=kb)

@dp.message(Command("help"))
async def help_handler(msg: types.Message):
    lang = get_user_lang(msg.from_user.language_code)
    await msg.answer(_(lang, "help"))

@dp.message(Command("encode"))
async def encode_handler(msg: types.Message):
    lang = get_user_lang(msg.from_user.language_code)
    text = msg.text.split(maxsplit=1)
    if len(text) < 2:
        await msg.reply(_(lang, "enter_text"))
        return
    encoded = encode_base64(text[1])
    store_access(encoded, msg.from_user.id)
    await msg.reply(f"🔐 <code>{encoded}</code>")

@dp.message(Command("decode"))
async def decode_handler(msg: types.Message):
    lang = get_user_lang(msg.from_user.language_code)
    parts = msg.text.split(maxsplit=1)
    if len(parts) < 2:
        await msg.reply(_(lang, "enter_base64"))
        return
    try:
        decoded = decode_base64(parts[1])
        await msg.reply(f"📨 {decoded}")
    except Exception:
        await msg.reply(_(lang, "decoding_error"))

@dp.message(Command("sendto"))
async def sendto_handler(msg: types.Message):
    lang = get_user_lang(msg.from_user.language_code)
    parts = msg.text.split(maxsplit=2)
    if len(parts) < 3 or not parts[1].startswith("@"):
        await msg.reply(_(lang, "sendto_usage"))
        return

    user = parts[1]
    text = parts[2]
    encoded = encode_base64(text)
    store_access(encoded, user)
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔓 Decrypt", callback_data=f"decrypt:{encoded}")]
    ])
    await msg.reply(f"🔐 Send this code:\n<code>{encoded}</code>", reply_markup=kb)

@dp.callback_query(F.data.startswith("decrypt:"))
async def decrypt_callback(callback: types.CallbackQuery):
    encoded = callback.data.split(":")[1]
    user_id = callback.from_user.id
    lang = get_user_lang(callback.from_user.language_code)

    try:
        with open("access.json", "r") as f:
            data = json.load(f)
        if str(user_id) in data.get(encoded, []):
            decoded = decode_base64(encoded)
            await callback.answer(_(lang, "decrypted"), show_alert=True)
            await callback.message.answer(f"📨 {decoded}")
        else:
            await callback.answer(_(lang, "not_for_you"), show_alert=True)
    except Exception:
        await callback.answer("❗️ Error")

@dp.callback_query(F.data.startswith("lang:"))
async def set_lang(callback: types.CallbackQuery):
    code = callback.data.split(":")[1]
    await callback.answer()
    await callback.message.answer(_(code, "start"))

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
