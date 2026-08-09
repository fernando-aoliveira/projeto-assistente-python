from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters
from utils.security import apenas_admin
from services.ai_service import AIService

# Instância única do serviço de IA
ai_service = AIService()

@apenas_admin
async def processar_mensagem_texto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto_usuario = update.message.text
    
    # Envia uma indicação visual no Telegram de que o bot está "digitando..."
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    # Processa a mensagem na IA
    resposta_ia = ai_service.gerar_resposta(texto_usuario)
    
    # Responde no Telegram
    try:
        await update.message.reply_text(resposta_ia, parse_mode="Markdown")
    except Exception:
        # Fallback caso a formatação em Markdown da IA venha com caracteres especiais não suportados pelo Telegram
        await update.message.reply_text(resposta_ia)

def get_message_handler():
    # Captura todas as mensagens de TEXTO que NÃO sejam comandos (que começam com /)
    return MessageHandler(filters.TEXT & (~filters.COMMAND), processar_mensagem_texto)