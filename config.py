from dotenv import load_dotenv
import os


load_dotenv()

# BOT_TOKEN = os.getenv("BOT_TOKEN")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
DATABASE = os.getenv("DATABASE")

DATABASE_URL = f"postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}/{DATABASE}"