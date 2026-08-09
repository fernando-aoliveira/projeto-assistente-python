import os
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_ADMIN_ID = os.getenv("TELEGRAM_ADMIN_ID")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")

# Validação básica ao subir a aplicação
if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN não foi configurado no arquivo .env!")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY não foi configurada no arquivo .env!")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL não foi configurada no arquivo .env!")

if TELEGRAM_ADMIN_ID:
    TELEGRAM_ADMIN_ID = int(TELEGRAM_ADMIN_ID)