from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from utils.security import apenas_admin

@apenas_admin
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    mensagem = (
        f"Olá, {user_name}! 👋\n\n"
        "Sou o seu **Assistente Pessoal**.\n"
        "A Fase 1 (Fundação e Conectividade) foi configurada com sucesso!\n\n"
        "Em breve terei suporte a IA, banco de dados e mensagens de voz."
    )
    await update.message.reply_text(mensagem, parse_mode="Markdown")

def get_start_handler():
    return CommandHandler("start", start_command)