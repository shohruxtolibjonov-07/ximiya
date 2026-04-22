import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

# Database yo'li — Docker uchun /app/data/ papkasida saqlanadi
DATABASE_PATH = os.getenv("DATABASE_PATH", "kimyo_bot.db")
DB_URL = f"sqlite+aiosqlite:///{DATABASE_PATH}"
