"""Instagram Utils"""

import re
from io import BytesIO

import instaloader
import requests
from telebot import TeleBot
from telebot.types import InputMediaPhoto, Message

from scripts.cookies_instagram_firefox import get_cookiefile, import_session

# Ejecuta el bloque __main__ del script importado
cookiefile = get_cookiefile()
SESSION_FILE = "session_file.json"

# Importa la sesión
loader = import_session(cookiefile, SESSION_FILE)


class InstagramUtils:
    """Instagram Utils"""

    def __init__(self, bot: TeleBot):
        self.bot = bot

    def is_instagram(self, url: str) -> bool:
        """Check if an Instagram Link (either post or reel)"""
        instagram_regex = (
            r"^(https?://)?(www\.)?instagram\.com/(p|reel)/[A-Za-z0-9_\-]+/?"
        )
        return re.match(instagram_regex, url) is not None

    def handle_instagram(self, message: Message, url):
        """Handler Instagram URL"""
        try:
            post_match = re.search(r"/p/([^/]+)", url)
            reel_match = re.search(r"/reel/([^/]+)", url)

            if post_match:
                shortcode = post_match.group(1)
            elif reel_match:
                shortcode = reel_match.group(1)
            else:
                self.bot.send_message(
                    message.from_user.id,
                    "Hay un error en la URL. Por favor, verifique e intente nuevamente.",
                )
                raise ValueError(
                    "La URL proporcionada no es una publicación ni un reel de Instagram."
                )

            post = instaloader.Post.from_shortcode(loader.context, shortcode)

            # Check type of post, donwload the content
            # send it to the user and delete the file locally

            if post.typename == "GraphImage":
                # print("GraphImage")
                response = requests.get(post.url, timeout=5000)
                photo = BytesIO(response.content)
                return self.bot.send_photo(message.from_user.id, photo)

            elif post.typename == "GraphVideo":
                # print("GraphVideo")
                video_url = post.video_url
                response = requests.get(video_url, timeout=5000)
                video_file = BytesIO(response.content)
                self.bot.send_video(
                    message.chat.id, video_file, caption="Video de instagram"
                )

            elif post.typename == "GraphSidecar":
                # print("GraphSidecar")
                media = []
                for sidecar_post in post.get_sidecar_nodes():
                    if sidecar_post.is_video:
                        # Download video locally, send it to the user and delete it
                        response = requests.get(sidecar_post.video_url, timeout=5000)
                        video = BytesIO(response.content)
                        media.append(InputMediaPhoto(video))
                    else:
                        response = requests.get(sidecar_post.display_url, timeout=5000)
                        photo = BytesIO(response.content)
                        media.append(InputMediaPhoto(photo))
                return self.bot.send_media_group(message.from_user.id, media)
            else:
                return self.bot.send_message(
                    message.from_user.id,
                    "No se puede procesar este tipo de publicación. Intente con otro.",
                )

        except instaloader.exceptions.InstaloaderException as e:
            self.bot.reply_to(
                message, f"Error al procesar el enlace de Instagram: {str(e)}"
            )
        except ValueError as e:
            self.bot.reply_to(message, str(e))
