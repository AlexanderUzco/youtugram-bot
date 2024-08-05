"""Youtube Utils"""

import os

import pytubefix
from pytubefix import YouTube
from telebot import TeleBot, types


class YoutubeUtils:
    """Youtube Bot Utils"""

    def __init__(self, user_data, bot: TeleBot):
        self.user_data = user_data
        self.bot = bot

    def handle_audio(self, user_id):
        """Handler Audio Case"""
        url = self.user_data[user_id]["url"]
        try:
            yt = YouTube(url)
            video_stream = yt.streams.filter(only_audio=True).first()
            out_file = video_stream.download()
            base = os.path.splitext(out_file)
            new_file = base[0] + ".mp3"
            os.rename(out_file, new_file)

            # Enviar el archivo de audio
            with open(new_file, "rb") as audio_file:
                self.bot.send_audio(
                    chat_id=user_id, audio=audio_file, title=yt.title, reply_markup=None
                )
        except pytubefix.exceptions.VideoUnavailable as e:
            self.bot.reply_to(
                user_id, f"Error al procesar el enlace de YouTube: {str(e)}"
            )
        finally:
            # Eliminar el archivo local si existe
            if os.path.exists(new_file):
                os.remove(new_file)
            self.user_data.pop(user_id, None)

    def handle_video(self, user_id):
        """Handler Video Case"""
        url = self.user_data[user_id]["url"]
        try:
            yt = YouTube(url)
            video_streams = yt.streams.filter(progressive=True).order_by("resolution")
            resolutions = {stream.resolution: stream for stream in video_streams}

            # Mostrar opciones de resolución
            markup = types.ReplyKeyboardMarkup(
                resize_keyboard=True, one_time_keyboard=True
            )
            for resolution in sorted(resolutions.keys(), reverse=True):
                item = types.KeyboardButton(f"Resolución: {resolution}")
                markup.add(item)
            markup.add(types.KeyboardButton("/cancel"))

            self.bot.send_message(
                user_id,
                "Elige una resolución para descargar el video:",
                reply_markup=markup,
            )

            self.user_data[user_id]["video_streams"] = resolutions

        except pytubefix.exceptions.VideoUnavailable as e:
            self.bot.reply_to(
                user_id, f"Error al procesar el enlace de YouTube: {str(e)}"
            )

    def handle_resolution_selection(self, message):
        """Handles the resolution selection by the user."""
        user_id = message.chat.id
        resolution_text = message.text
        resolution = resolution_text.split(": ")[1]

        self.bot.send_message(user_id, "Video Descargandose, por favor espere...")

        if resolution in self.user_data[user_id]["video_streams"]:
            selected_stream = self.user_data[user_id]["video_streams"][resolution]
            out_file = selected_stream.download()

            try:
                # Enviar el archivo por Telegram
                with open(out_file, "rb") as video_file:
                    self.bot.send_video(user_id, video_file)
            except pytubefix.exceptions.VideoUnavailable as e:
                self.bot.reply_to(user_id, f"Error al enviar el video: {str(e)}")
            finally:
                # Eliminar el archivo local
                if os.path.exists(out_file):
                    os.remove(out_file)
                del self.user_data[user_id]  # Limpiar datos del usuario

        else:
            self.bot.send_message(
                user_id, "Selección inválida. Por favor, elige una resolución válida."
            )
