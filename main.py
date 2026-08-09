import logging
from telegram.ext import ApplicationBuilder
from config.settings import TELEGRAM_TOKEN
from handlers.start_handler import get_start_handler
from handlers.message_handler import get_message_handler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def main():
    print("Iniciando o Assistente Pessoal com IA no Telegram...")
    
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    # Registra os handlers
    app.add_handler(get_start_handler())
    app.add_handler(get_message_handler())  # <--- NOVO HANDLER REGISTRADO
    
    print("Bot rodando com Inteligência Artificial! Faça uma pergunta no Telegram.")
    app.run_polling()

if __name__ == "__main__":
    main()