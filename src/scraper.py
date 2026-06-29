import os
import json
import logging
import asyncio
from pathlib import Path

from datetime import datetime

from telethon import TelegramClient
from telethon.sync import TelegramClient
from telethon.errors import FloodWaitError
from dotenv import load_dotenv

load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
PHONE_NUMBER = os.getenv("PHONE_NUMBER")


CHANNELS = [

    "CheMed123",

    "lobelia4cosmetics",

    "tikvahpharma"

]

#folder structure
RAW_DATA = Path("data/raw/telegram_messages")
IMAGE_DATA = Path("data/raw/images")
LOG_DIR = Path("logs")

RAW_DATA.mkdir(parents=True, exist_ok=True)
IMAGE_DATA.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR / "scraper.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

#Telegram client
client = TelegramClient(
    "session",
    API_ID,
    API_HASH
)
client.start(phone=PHONE_NUMBER)

logger.info("Connected to Telegram")

today = datetime.now().strftime("%Y-%m-%d")
today_folder = RAW_DATA / today
today_folder.mkdir(parents=True, exist_ok=True)

# scrape channel
for channel in CHANNELS:

    logger.info(f"Scraping channel: {channel}")

    messages = []

    image_folder = IMAGE_DATA / channel
    image_folder.mkdir(parents=True, exist_ok=True)

    try:

        entity = client.get_entity(channel)

        for message in client.iter_messages(entity):

            image_path = None

            
            # Download Images
            if message.photo:

                image_file = image_folder / f"{message.id}.jpg"

                client.download_media(
                    message,
                    file=image_file
                )

                image_path = str(image_file)

          
            # Extract Message Information
            msg = {
                "message_id": message.id,
                "date": (
                    message.date.isoformat()
                    if message.date else None
                ),
                "text": message.message,
                "views": message.views,
                "forwards": message.forwards,
                "has_media": message.photo is not None,
                "image_path": image_path
            }

            messages.append(msg)

        # Save JSON
        output_file = today_folder / f"{channel}.json"

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                messages,
                f,
                indent=4,
                ensure_ascii=False
            )

        logger.info(
            f"{channel}: {len(messages)} messages saved."
        )

    except FloodWaitError as e:

        logger.error(
            f"Flood wait. Sleep for {e.seconds} seconds."
        )

    except Exception as e:

        logger.error(
            f"Error scraping {channel}: {e}"
        )

logger.info("Scraping completed.")

client.disconnect()

print("Finished scraping.")
