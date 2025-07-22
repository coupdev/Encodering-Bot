from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from i18n import i18n
from utils import encode, decode, store_message, get_message
from aiogram.fsm.context import FSMContext

router = Router()

@router.message(F.text.startswith("/start"))
async def start(msg: Message, state: FSMContext):
    lang = i18n.get_user_lang(msg.from_user.id)
    await msg.answer(i18n.t(lang, "start"))

@router.message(F.text.startswith("/help"))
async def help_cmd(msg: Message):
    lang = i18n.get_user_lang(msg.from_user.id)
    await msg.answer(i18n.t(lang, "help"))

@router.message(F.text.startswith("/lang"))
async def change_lang(msg: Message):
    await msg.answer("🌐 Choose your language:", reply_markup=i18n.language_keyboard())

@router.callback_query(F.data.startswith("lang:"))
async def set_lang(callback: CallbackQuery):
    lang = callback.data.split(":")[1]
    i18n.set_user_lang(callback.from_user.id, lang)
    await callback.answer(i18n.t(lang, "language_set"), show_alert=True)

@router.message(F.text.startswith("/encode"))
async def handle_encode(msg: Message):
    lang = i18n.get_user_lang(msg.from_user.id)
    text = msg.text.split(" ", 1)[1] if " " in msg.text else None
    if not text:
        return await msg.reply(i18n.t(lang, "enter_text"))
    encoded = encode(text)
    store_message(encoded, str(msg.from_user.id))
    await msg.answer(f"🔐 <code>{encoded}</code>")

@router.message(F.text.startswith("/decode"))
async def handle_decode(msg: Message):
    lang = i18n.get_user_lang(msg.from_user.id)
    text = msg.text.split(" ", 1)[1] if " " in msg.text else None
    if not text:
        return await msg.reply(i18n.t(lang, "enter_base64"))
    try:
        decoded = decode(text)
        await msg.reply(f"📨 {decoded}")
    except:
        await msg.reply(i18n.t(lang, "decoding_error"))

@router.message(F.text.startswith("/sendto"))
async def handle_sendto(msg: Message):
    lang = i18n.get_user_lang(msg.from_user.id)
    parts = msg.text.split(" ")
    if len(parts) < 3:
        return await msg.reply(i18n.t(lang, "sendto_usage"))
    username = parts[1]
    message_text = " ".join(parts[2:])
    encoded = encode(message_text)
    store_message(encoded, username)
    await msg.answer(f"🔐 Send this to the interlocutor:\n<code>{encoded}</code>")

@router.callback_query(F.data.startswith("decrypt:"))
async def decrypt_message(callback: CallbackQuery):
    lang = i18n.get_user_lang(callback.from_user.id)
    encoded = callback.data.split(":", 1)[1]
    result = get_message(encoded, str(callback.from_user.id))
    if result:
        await callback.answer(i18n.t(lang, "decrypted"), show_alert=True)
        await callback.message.answer(f"📨 {result}")
    else:
        await callback.answer(i18n.t(lang, "not_for_you"), show_alert=True)

def register_handlers(dp):
    dp.include_router(router)
