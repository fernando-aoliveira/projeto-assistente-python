import logging
from telegram.ext import ApplicationBuilder
from config.settings import TELEGRAM_TOKEN
from database.connection import init_db  # <--- IMPORTAÇÃO DA INICIALIZAÇÃO
from handlers.start_handler import get_start_handler
from handlers.message_handler import get_message_handler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def main():
    print("Iniciando o Assistente Pessoal...")
    
    # 1. Inicializa e garante que as tabelas existem no PostgreSQL
    init_db()
    
    # 2. Constrói a aplicação do bot
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    # 3. Registra os handlers
    app.add_handler(get_start_handler())
    app.add_handler(get_message_handler())
    
    print("Bot rodando! Conectado ao PostgreSQL com sucesso.")
    app.run_polling()

if __name__ == "__main__":
    main()