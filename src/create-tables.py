from pathlib import Path
from sqlalchemy import text

from database import engine


def create_tables():
    # Path to schema.sql
    schema_path = Path(__file__).parent.parent / "sql" / "schema.sql"

    
    with open(schema_path, "r", encoding="utf-8") as file:
        schema = file.read()

   
    with engine.connect() as connection:
        connection.execute(text(schema))
        connection.commit()

    print("✅ Database tables created successfully!")


if __name__ == "__main__":
    create_tables()