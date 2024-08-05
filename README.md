# Telegram YouTube-Instagram Downloader Bot

Este bot de Telegram permite a los usuarios descargar videos y audios desde YouTube. Actualmente, la funcionalidad para Instagram está en desarrollo.

## Funcionalidades (Youtube):

- **Descargar Audio:** Permite descargar el audio de un video de YouTube en formato MP3.
- **Descargar Video:** Permite descargar un video de YouTube en la resolución más alta disponible.
- **Cancelar Proceso:** Opción para cancelar la descarga en curso.

## Funcionalidades (Instagram)

- **Descargar Reels:** Permite reels de instagram.
- **Descargar imagenes:** Permite descargar imagenes de instagram.

## Requisitos para Instagram

> [!WARNING]
> **Uso de la Sesión de Instagram:** El bot utiliza la sesión de Instagram extraída de Firefox para acceder a Instagram. Ten en cuenta que Instagram puede considerar el uso de esta sesión como sospechoso, lo que podría llevar a la suspensión o bloqueo de la cuenta asociada. Por lo tanto, se recomienda utilizar una cuenta de Instagram dedicada exclusivamente para este propósito. No utilices una cuenta que uses regularmente o que no estés dispuesto a perder. Al utilizar este software, aceptas y entiendes que operas bajo tu propio riesgo y responsabilidad.

Para que el bot funcione con Instagram, es necesario seguir estos pasos:

1. **Inicia Sesión en Instagram en Firefox:**

   - Asegúrate de estar logueado en Instagram en el navegador Firefox.

2. **Guardar la Sesión de Firefox:**
   - Una vez iniciada la session en Firefox el bot correra automaticamente el script `scripts/cookies_instagram_firefox.py` para extraer y guardar la sesión de Firefox. Este script toma la sesión activa de Instagram en Firefox y la guarda en un archivo que luego será utilizado por el bot para acceder a Instagram.

## Cómo Empezar

Sigue estos pasos para configurar y ejecutar el bot:

### 1. Clona el Repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd <NOMBRE_DEL_DIRECTORIO>
```

## 2. Crea un Archivo .env

Crea un archivo .env en la raíz del proyecto y agrega tu token de Telegram:

```bash
TELEGRAM_TOKEN=tu_token_de_telegram
```

### Para configurar el bot de Telegran puedes seguir la siguiente guia: [Chatbot Telegram](https://sendpulse.com/latam/knowledge-base/chatbot/telegram/create-telegram-chatbot)

## 3. Instala las Dependencias

Asegúrate de tener pip instalado, luego instala las dependencias necesarias:

```bash
pip install -r requirements.txt
```

## 4. Ejecuta el Bot

Ejecuta el bot usando Python:

```bash
python bot.py
```

## 5. Usa el Bot

Puedes comenzar buscando el bot que creaste en Telegram y comenzar con el comando /start

Luego puedes enviar algun link de Youtube o Instagram

En el caso de Youtube te pedira seleccionar si deseas descargar el audio o el video

En el caso de Instagram de Descargara el contenido del la url que le envies

# Estructura del Proyecto

1. bot.py: Archivo principal que contiene la lógica del bot.
2. src/youtube_utils.py: Contiene la clase YoutubeUtils para manejar la descarga de videos y audios desde YouTube.
3. src/instagram_utils.py: Contiene la clase InstagramUtils para manejar las descarga del contenido de Instagram
4. scripts/cookies_instagram_firefox.py: Script utilizado para almacenar la session de instagram en el navegador Firefox
5. .env: Archivo para almacenar el token de Telegram.
6. requirements.txt: Lista de dependencias del proyecto.
