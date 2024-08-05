"""
Telegram bot
"""

import os

import instaloader
import telebot
from dotenv import load_dotenv
from telebot.types import Message

from src.instagram_utils import InstagramUtils
from src.youtube_utils import YoutubeUtils

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

user_data = {}

# Telegram Bot
bot = telebot.TeleBot(TELEGRAM_TOKEN, parse_mode=None)

# Instagram Loader
loader = instaloader.Instaloader()

youtube_utils = YoutubeUtils(user_data, bot)
instagram_utils = InstagramUtils(bot=bot)


## BOT MESSAGE HANDLER


@bot.message_handler(commands=["start"])
def start_flow(message: Message):
    """Start Bot"""
    chat_id = message.chat.id
    bot.send_message(
        chat_id, "Hola!, por favor envia un link de Youtube o Instagram para procesarlo"
    )


@bot.message_handler(commands=["cancel"])
def cancel_flow(message: Message):
    """Cancel flow function"""

    user_id = message.from_user.id
    if user_id in user_data:
        user_data.pop(user_id)
        bot.send_message(user_id, "Proceso Cancelado!")


@bot.message_handler(func=lambda message: "Resolución:" in message.text)
def resolution_handler(message: Message):
    """Select Resolution"""
    youtube_utils.handle_resolution_selection(message)


@bot.message_handler(func=lambda m: True)
def handler_message(message: Message):
    """Send message to user"""
    url = message.text
    user_id = message.from_user.id

    if user_id in user_data:
        if message.text == "Descargar MP3":
            youtube_utils.handle_audio(user_id)
            return
        elif message.text == "Descargar Video":
            youtube_utils.handle_video(user_id)
            return
        else:
            bot.reply_to(message, "Por favor, elige una opción válida.")
            return

    if youtube_utils.is_youtube(url):
        user_data[user_id] = {"url": url}
        markup = telebot.types.ReplyKeyboardMarkup(
            resize_keyboard=True, one_time_keyboard=True
        )
        item1 = telebot.types.KeyboardButton("Descargar MP3")
        item2 = telebot.types.KeyboardButton("Descargar Video")
        item3 = telebot.types.KeyboardButton("/cancel")
        markup.add(item1, item2, item3)
        bot.send_message(
            message.chat.id,
            "¿Cómo deseas descargarlo?",
            reply_markup=markup,
        )
    elif instagram_utils.is_instagram(url):
        # bot.send_message(
        #     user_id, "De momento no podemos descargar contenido de Instagram..."
        # )
        # return
        instagram_utils.handle_instagram(message, url)
    else:
        bot.reply_to(
            message,
            "Enlace no soportado. Por favor, envía un enlace de YouTube o Instagram.",
        )


bot.infinity_polling()
