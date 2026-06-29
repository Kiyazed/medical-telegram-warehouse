import json
from pathlib import Path

from sqlalchemy import text

from database import engine



DATA_FOLDER = Path("data/raw/telegram_messages")


def ingest_json():

    with engine.begin() as connection:

       
        json_files = DATA_FOLDER.rglob("*.json")

        for json_file in json_files:

            print(f"Reading {json_file.name}")

            channel_name = json_file.stem

           
            result = connection.execute(
                text("""
                    SELECT id
                    FROM channels
                    WHERE channel_name=:name
                """),
                {"name": channel_name},
            ).fetchone()

            if result:

                channel_id = result[0]

            else:

                insert = connection.execute(
                    text("""
                        INSERT INTO channels(channel_name)
                        VALUES(:name)
                        RETURNING id
                    """),
                    {"name": channel_name},
                )

                channel_id = insert.fetchone()[0]

            # Read messages
            with open(json_file, encoding="utf-8") as file:
                messages = json.load(file)

            # Insert messages
            for msg in messages:

                connection.execute(
                    text("""
                    INSERT INTO messages(

                        message_id,
                        channel_id,
                        message_text,
                        message_date,
                        views,
                        forwards,
                        has_media,
                        image_path

                    )

                    VALUES(

                        :message_id,
                        :channel_id,
                        :message_text,
                        :message_date,
                        :views,
                        :forwards,
                        :has_media,
                        :image_path

                    )
                    """),
                    {

                        "message_id": msg["message_id"],
                        "channel_id": channel_id,
                        "message_text": msg["text"],
                        "message_date": msg["date"],
                        "views": msg["views"],
                        "forwards": msg["forwards"],
                        "has_media": msg["has_media"],
                        "image_path": msg["image_path"],

                    },
                )

    print("✅ Data successfully inserted into PostgreSQL!")


if __name__ == "__main__":
    ingest_json()