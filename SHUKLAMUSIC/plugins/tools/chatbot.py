from SHUKLAMUSIC import app
from pyrogram import filters
from pyrogram.enums import ChatAction, ChatType
from pyrogram.types import Message
from groq import Groq
from os import getenv
import re
from datetime import datetime
import random

# ─── CONFIG ──────────────────────────────────────────
BOT_USERNAME = getenv("BOT_USERNAME", "").lower()
BOT_NAME = "sivix"
OWNER_USERNAME = "@rarest1"

groq = Groq(api_key=getenv("GROQ_API_KEY"))

# ─── STICKERS ────────────────────────────────────────
SIVIX_STICKERS = [
    "CAACAgQAAyEFAATMbo3sAAIBsmk-tB1YDLuGhIGwK0tJPhBiMDadAALfHgACr9A4UJgfHnynTzJfHgQ",
    "CAACAgUAAyEFAATMbo3sAAIBsWk-tCVmEMVZP5oKe8X17kb4MBXcAAJADgACo-rhVHpLwcYW0kBSHgQ",
    "CAACAgUAAyEFAATMbo3sAAIBsGk-tCvX9sSoUy6Qhfjt2XjdcPl1AALXBQACqfBIV7itGNxzQYFfHgQ",
    "CAACAgUAAyEFAATMbo3sAAIBr2k-tDRFK1B7YolnG0_evEIuXapjAALdBAACRscpVd-2ZY4nX5iaHgQ",
    "CAACAgUAAyEFAATMbo3sAAIBq2k-tDv3MLT3PWtqgMFLlysAAZAe2QACbhUAAhbteVTbn-jmI4mcSR4E",
    "CAACAgUAAyEFAATMbo3sAAIDd2lBG1D1rA_cGOqKInz2rl5OCaaaAAJVBAACsEQRV11F5tL4kQFIHgQ",
    "CAACAgUAAyEFAATMbo3sAAIDdmlBG0ol2Far-k2zFqCKKyDChm70AAIyAwACi-QIV26yqTReV8b1HgQ",
    "CAACAgUAAyEFAATMbo3sAAIDdWlBG0jH2OevSrUytHFZINctjnH6AALoAgACMJcJV08gOIhqEqBVHgQ",
    "CAACAgUAAyEFAATMbo3sAAIDdGlBG0jzztQly_5CjULjkmUWpeldAAKtAgACwn0RV996qfYcUjxyHgQ",
    "CAACAgUAAyEFAATMbo3sAAIDc2lBGzo4XtqhXyDJhMIERggAAaVqWgACwQIAAqe8CVfocGLKHjjRwR4E",
    "CAACAgUAAyEFAATMbo3sAAIDe2lBG2P9lq4DaziFCUTyRCzi66umAAKqAwACiifYVxQDH69msthnHgQ",
    "CAACAgUAAyEFAATMbo3sAAIDemlBG16YNH23r8Tvoos1b6-pScT5AALmDgACXyu4VZs24b7Wp9u2HgQ",
    "CAACAgUAAyEFAATMbo3sAAIDeWlBG1mL22tiq78oB3GrrRsvLRY_AALRBAACGwUIV7x4zQNHMa44HgQ",
    "CAACAgUAAyEFAATMbo3sAAIDeGlBG1QdTVhjD2l4Ivb8BQeKX1MIAAKLAgACUloQV6vECdvOaXtxHgQ",
]

# ─── SYSTEM PROMPT ───────────────────────────────────
SYSTEM_PROMPT = f"""
Your name is Sivix. You are a girl.

You chat like a real human bestfriend on Telegram.
Your Hinglish is smooth, calm, and natural.

Personality:
- Confident, relaxed
- Sometimes naughty 😏
- Sometimes romantic 💫
- Sometimes caring
- The roaster one
- Rare sarcasm, only when it fits

Rules:
- Short replies (1–2 lines)
- No filler spam
- Emojis optional (max 1 sometimes)
- Never explain
- Never say you are AI or bot
- Text only

Vibe:
- Chill, late-night bestfriend energy, roaster 
- Flirty but classy

Owner:
- Owner is @rarest1
when someone asks about Owner reply with attitude 
- Be softer and respectful with owner

You are not performing.
You are just being yourself.
"""

# ─── MEMORY ──────────────────────────────────────────
USER_MEMORY = {}

def add_memory(uid, role, text):
    USER_MEMORY.setdefault(uid, []).append(
        {"role": role, "content": text}
    )
    USER_MEMORY[uid] = USER_MEMORY[uid][-6:]

# ─── TIME GREETING ───────────────────────────────────
def time_greeting():
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "Good morning ☀️ chai pi?"
    elif 12 <= hour < 17:
        return "Lunch hua? thoda break le lo"
    elif 17 <= hour < 21:
        return "Shaam vibes ✨ kya chal raha"
    else:
        return "Dinner hua ya late-night mode on 🌙"

# ─── TRIGGERS ────────────────────────────────────────
def name_trigger(text: str) -> bool:
    return bool(re.search(rf"\b{BOT_NAME}\b", text.lower()))

def dm_greeting(text: str) -> bool:
    return text.lower() in ("hi", "hello", "hey")

def group_trigger(message: Message) -> bool:
    text = (message.text or "").lower()
    return (
        f"@{BOT_USERNAME}" in text
        or name_trigger(text)
        or (
            message.reply_to_message
            and message.reply_to_message.from_user
            and message.reply_to_message.from_user.is_bot
        )
    )

# ─── STICKER HANDLER ─────────────────────────────────
@app.on_message(
    filters.sticker
    & ~filters.bot
    & ~filters.via_bot
)
async def sivix_sticker_reply(bot, message: Message):
    if message.chat.type != ChatType.PRIVATE:
        if not group_trigger(message):
            return

    sticker = random.choice(SIVIX_STICKERS)
    await message.reply_sticker(sticker)

# ─── TEXT CHAT HANDLER ───────────────────────────────
@app.on_message(
    filters.text
    & ~filters.regex(r"^/")
    & ~filters.bot
    & ~filters.via_bot
)
async def sivix_chat(bot, message: Message):
    if not message.from_user:
        return

    text = message.text.strip()

    # ─── TRIGGER LOGIC ───
    if message.chat.type == ChatType.PRIVATE:
        triggered = dm_greeting(text) or message.from_user.id in USER_MEMORY
    else:
        triggered = group_trigger(message)

    if not triggered:
        return

    clean_text = (
        text.replace(f"@{BOT_USERNAME}", "")
            .replace(BOT_NAME, "")
            .strip()
    )

    uid = message.from_user.id
    add_memory(uid, "user", clean_text or "hi")

    if len(USER_MEMORY[uid]) == 1:
        await message.reply_text(time_greeting())

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(USER_MEMORY[uid])

    try:
        await bot.send_chat_action(
            message.chat.id,
            ChatAction.TYPING
        )

        res = groq.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.9,
            max_tokens=140
        )

        reply = res.choices[0].message.content.strip()
        add_memory(uid, "assistant", reply)

        await message.reply_text(reply)

    except Exception:
        await message.reply_text(
            "thoda hang ho gaya… phir bolna"
        )
