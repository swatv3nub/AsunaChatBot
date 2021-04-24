import asyncio
import re
import aiohttp
from config import TOKEN, ARQ_API, BOT_ID as bot_id
from pyrogram import Client, filters, __version__
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Python_ARQ import ARQ

asuna = Client(
    ":memory:",
    bot_token=TOKEN,
    api_id=6,
    api_hash="eb06d4abfb49dc3eeb1aeb98ae0f581e",
)

arq = ARQ(ARQ_API)

mode = None

"""
async def chatbot(query):
    asuna = await arq.luna(query)
    response = asuna.response
    return response
"""    
async def chatbot(query):
    url = f"https://elianaapi.herokuapp.com/eliana/chatbot?text={query}&name=Asuna"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as res:
            res = await res.json()
            text = res["message"]
            return text
    
start_text = """Hello, I am **Asuna [アスナ]**, An Intelligent ChatBot. If You Are Feeling Lonely, You can Always Come to me and Chat With Me!"""

info_text = f"""Build To Be One of The Cutest ChatBot,\n**Asuna [アスナ]** is One of the Anime Themed Chatbot in Telegram.

**Asuna [アスナ]** System Info:
    **• Host:** `Heroku`
    **• OS:** `Debian`
    **• Python Version:** `3.9.1`
    **• Library Used:** `Pyrogram`
    **• Library Version:** `{__version__}`
    **• Owner | Bot Dev:** @MaskedVirus
    **• Self-Trained Model using BrainShop •**
    """
    
asunapic = "https://telegra.ph/file/cb3b9a091ee2480fc2cea.jpg"
    
keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Share Me",
                        url="tg://msg?text=Hi+%E2%9D%A4%EF%B8%8F%2C%0D%0AI+Found+an+Cute+and+Unique+ChatBot+By+%40MaskedVirus.+%0D%0ABot+Username+%3A+%40AsunaChatBot",
                    ),
                    InlineKeyboardButton(
                        text="Info",
                        callback_data="info")
                ]
            ]
        )

helpo = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Back",
                        callback_data="start_back",
                    )
                ]
            ]
        )        

@asuna.on_message(filters.command(["start" , "start@AsunaChatBot"]))
async def start(_, message):
    if message.chat.type == "private":
        await message.reply_photo(photo=asunapic, caption=start_text, reply_markup=keyboard, parse_mode="markdown")
    else:
        await message.reply_text("**Asuna [アスナ]** is Alive\nowo :3", parse_mode="markdown")

@asuna.on_callback_query(filters.regex("start_back"))
async def start_back(_, CallbackQuery):
    await asuna.send_photo(
        CallbackQuery.message.chat.id,
        photo=asunapic,
        caption=start_text,
        reply_markup=keyboard
    )

    await CallbackQuery.message.delete()
    

@asuna.on_callback_query(filters.regex("info"))
async def start_info(_, CallbackQuery):
    await asuna.send_photo(
        CallbackQuery.message.chat.id,
        photo=asunapic,
        caption=info_text,
        reply_markup=helpo
    )

    await CallbackQuery.message.delete()

@asuna.on_message(filters.regex("(?i)eliza"))
async def eliza(_, message):
    await message.reply_text("Wait Who?")
    return

@asuna.on_message(~filters.edited & filters.private & ~filters.command(["start" , "start@AsunaChatBot"]))
async def inbox(_, message):
    if not message.text:
        return
    query = message.text
    if len(query) > 50:
        return
    try:
        res = await chatbot(query)
        await asyncio.sleep(1)
    except Exception as e:
        res = str(e)
    await message.reply_text(res)
    await asuna.send_chat_action(message.chat.id, "cancel")
        
@asuna.on_message(~filters.edited & ~filters.private & ~filters.command(["start", "start@AsunaChatBot"]))
async def group(_, message):
    if message.reply_to_message:
        if not message.reply_to_message.from_user.id == bot_id:
            return
        await asuna.send_chat_action(message.chat.id, "typing")
        if not message.text:
            query = "Hello"
        else:
            query = message.text
        if len(query) > 50:
            return
        try:
            res = await chatbot(query)
            await asyncio.sleep(1)
        except Exception as e:
            res = str(e)
        await message.reply_text(res)
        await asuna.send_chat_action(message.chat.id, "cancel")
    else:
        if message.text:
            query = message.text
            if len(query) > 50:
                return
            if re.search("[.|\n]{0,}[a|A][s|S][u|U][n|N][a|A][.|\n]{0,}", query):
                await asuna.send_chat_action(message.chat.id, "typing")
                try:
                    res = await chatbot(query)
                    await asyncio.sleep(1)
                except Exception as e:
                    res = str(e)
                await message.reply_text(res)
                await asuna.send_chat_action(message.chat.id, "cancel")

print(
    """
-------------------------------------
| Turned the Cutiepie Asuna Online! |
-------------------------------------

"""
)


asuna.run()
