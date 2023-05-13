# Strictly Pyrogram version 1.9.2
import asyncio
import re
import os
import aiohttp
import requests
import subprocess
from config import TOKEN, BOT_ID
from pyrogram import Client, filters, __version__
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from google_trans_new import google_translator

asuna = Client(
    ":memory:",
    bot_token=TOKEN,
    api_id=6,
    api_hash="eb06d4abfb49dc3eeb1aeb98ae0f581e",
)

mode = None

async def chatbot(query):
     translator = google_translator()
    #  qw, aw = translator.detect(query)
    #  if qw != "en":
    #    query = translator.translate(query,lang_tgt='en')
     api = f"http://api.brainshop.ai/get?bid=155827&key=tVhEcHqwrXqtCNZT&uid=73948&msg={query}"
     res = requests.get(api).json()
     data = res['cnt']
    #  if qw != "en":
    #    aww = translator.translate(data,lang_tgt='en')
    #    return aww
     return data


start_text = """Hello, I am **Asuna [アスナ]**, An Intelligent ChatBot. If You Are Feeling Lonely, You can Always Come to me and Chat With Me!"""

info_text = f"""Build To Be One of The Cutest ChatBot,\n**Asuna [アスナ]** is One of the Anime Themed Chatbot in Telegram.

**Asuna [アスナ]** System Info:
    **• Host:** ``
    **• OS:** `Ubuntu`
    **• Python Version:** `3.9.5`
    **• Library Used:** `Pyrogram`
    **• Library Version:** `{__version__}`
    **• Owner | Bot Dev:** @MaskedVirus
    **• Self-Trained Model using BrainShop •**

    __And Yes, I don't Reply to Stickers__
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
    if message.from_user.id == 1167145475:
        await message.reply_photo(photo=asunapic, caption="**Hello Boss,**\n\n Asuna [アスナ] at your service", reply_markup=keyboard, parse_mode="markdown")
    else:
        if message.chat.type == "private":
            await message.reply_photo(photo=asunapic, caption=start_text, reply_markup=keyboard, parse_mode="markdown")
        else:
            await message.reply_text("**Asuna [アスナ]** is Alive\nowo :3", parse_mode="markdown")

@asuna.on_message(filters.command(["term", "sh"]))
async def terminal(client, message):
    if len(message.text.split()) == 1:
        await message.reply(f"Usage: `/sh echo owo`")
        return
    args = message.text.split(None, 1)
    teks = args[1]
    if "\n" in teks:
        code = teks.split("\n")
        output = ""
        for x in code:
            shell = re.split(""" (?=(?:[^'"]|'[^']*'|"[^"]*")*$)""", x)
            try:
                process = subprocess.Popen(
                    shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE
                )
            except Exception as err:
                print(err)
                await message.reply(
                    """
**Error:**
```{}```
""".format(
                        err
                    )
                )
            output += "**{}**\n".format(code)
            output += process.stdout.read()[:-1].decode("utf-8")
            output += "\n"
    else:
        shell = re.split(""" (?=(?:[^'"]|'[^']*'|"[^"]*")*$)""", teks)
        for a in range(len(shell)):
            shell[a] = shell[a].replace('"', "")
        try:
            process = subprocess.Popen(
                shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
        except Exception as err:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            errors = traceback.format_exception(
                etype=exc_type, value=exc_obj, tb=exc_tb
            )
            await message.reply("""**Error:**\n```{}```""".format("".join(errors)))
            return
        output = process.stdout.read()[:-1].decode("utf-8")
    if str(output) == "\n":
        output = None
    if output:
        if len(output) > 4096:
            with open("output.txt", "w+") as file:
                file.write(output)
            await client.send_document(
                message.chat.id,
                "output.txt",
                reply_to_message_id=message.message_id,
                caption="`Output file`",
            )
            os.remove("output.txt")
            return
        await message.reply(f"**Output:**\n```{output}```", parse_mode="markdown")
    else:
        await message.reply("**Output:**\n`No Output`")
    

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

@asuna.on_message(~filters.edited & ~filters.sticker & filters.private & ~filters.command(["start" , "start@AsunaChatBot"]))
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
        
@asuna.on_message(~filters.edited & ~filters.sticker & ~filters.private & ~filters.command(["start", "start@AsunaChatBot"]))
async def group(_, message):
    if message.reply_to_message:
        if not message.reply_to_message.from_user.id == BOT_ID:
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
