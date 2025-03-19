import sqlite3
from config import config

database = "data/pictures.db"

def init_db():
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    for target in config.endpoints.keys():
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {target} (
                image TEXT PRIMARY KEY
            )
        """)
    conn.commit()
    conn.close()


def image_exists(target, image):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute(f"SELECT 1 FROM {target} WHERE image = ?", (image,))
    img = cursor.fetchone()  # Retorna None si no hay resultados
    conn.close()
    return img is not None


def insert_image(target, image):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute(f"INSERT OR IGNORE INTO {target} (image) VALUES (?)", (image,))
    conn.commit()
    conn.close()
