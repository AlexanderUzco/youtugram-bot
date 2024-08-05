"""
Telegram bot
"""

import os
import re
from io import BytesIO

import instaloader
import requests
import telebot
from dotenv import load_dotenv
from pytubefix import YouTube
from telebot.types import KeyboardButton, Message, ReplyKeyboardMarkup

from src.youtube_utils import YoutubeUtils

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

user_data = {}

# Telegram Bot
bot = telebot.TeleBot(TELEGRAM_TOKEN, parse_mode=None)

# Instagram Loader
loader = instaloader.Instaloader()

youtube_utils = YoutubeUtils(user_data, bot)


def is_youtube(url: str) -> bool:
    """Check if a youtube link"""
    youtube_regex = r"(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/)"
    return re.match(youtube_regex, url) is not None


def is_instagram(url: str) -> bool:
    """Check if an instagram Link"""
    instagram_regex = r"(https?://)?(www\.)?instagram\.com/p/"
    return re.match(instagram_regex, url) is not None


def handle_instagram(message: Message, url):
    """Handler instagram Url"""
    try:
        shortcode = re.search(r"/p/([^/]+)", url).group(1)
        post = instaloader.Post.from_shortcode(loader.context, shortcode)

        if post.is_video:
            # Descargar video
            video_url = post.video_url
            response = requests.get(video_url, timeout=5000)
            video_file = BytesIO(response.content)
            bot.send_video(
                message.chat.id, video_file, caption="Este es un reel de Instagram."
            )
        else:
            # Descargar imagen
            image_url = post.url
            response = requests.get(image_url, timeout=5000)
            image_file = BytesIO(response.content)
            bot.send_photo(
                message.chat.id,
                image_file,
                caption="Esta es una publicación de Instagram.",
            )

        markup = ReplyKeyboardMarkup(row_width=10)
        markup.add(KeyboardButton("Descargar"))

        # Enviar botón de descarga
        bot.send_message(
            message.chat.id, "Haz clic en el botón para descargar.", reply_markup=markup
        )

    except instaloader.exceptions.InstaloaderException as e:
        bot.reply_to(message, f"Error al procesar el enlace de Instagram: {str(e)}")


def handle_youtube(message: Message, url):
    """Handler Youtube URL"""
    try:
        yt = YouTube(url)
        video_stream = yt.streams.get_highest_resolution()

        # Descargar video
        video_file = BytesIO()
        video_stream.stream_to_file(video_file, filename="temp_video.mp4")

        # Enviar video
        video_file.seek(0)  # Rewind the file
        bot.send_video(
            message.chat.id, video_file, caption=f"Video de YouTube: {yt.title}"
        )

        # No es necesario borrar el archivo ya que BytesIO no crea un archivo físico
        # Si usas un archivo físico, usarías `os.remove('temp_video.mp4')`

    except instaloader.exceptions.InstaloaderException as e:
        bot.reply_to(message, f"Error al procesar el enlace de YouTube: {str(e)}")


## BOT MESSAGE HANDLER
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

    if is_youtube(url):
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
    elif is_instagram(url):
        bot.send_message(
            user_data, "De momento no podemos descargar contenido de Instagram..."
        )
        return
        # handle_instagram(message, url)
    else:
        bot.reply_to(
            message,
            "Enlace no soportado. Por favor, envía un enlace de YouTube o Instagram.",
        )


bot.infinity_polling()
