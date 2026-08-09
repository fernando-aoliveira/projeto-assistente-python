from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters
from utils.security import apenas_admin
from services.ai_service import AIService
from services.db_service import DBService

ai_service = AIService()

@apenas_admin
async def processar_mensagem_texto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    texto_usuario = update.message.text
    
    # 1. Garante que o usuário existe no PostgreSQL
    DBService.salvar_ou_atualizar_usuario(
        user_id=user.id, 
        primeiro_nome=user.first_name, 
        username=user.username
    )
    
    # 2. Salva a nova mensagem enviada pelo usuário no banco
    DBService.salvar_mensagem(user_id=user.id, role="user", conteudo=texto_usuario)
    
    # 3. Animação de "digitando..." no Telegram
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    # 4. Busca o histórico recente no PostgreSQL (incluindo a mensagem atual)
    historico = DBService.obter_historico_recente(user_id=user.id, limite=10)
    
    # 5. Gera a resposta da IA com base no histórico permanente
    resposta_ia = ai_service.gerar_resposta(historico)
    
    # 6. Salva a resposta gerada pela IA no PostgreSQL
    DBService.salvar_mensagem(user_id=user.id, role="assistant", conteudo=resposta_ia)
    
    # 7. Envia para o usuário no Telegram
    try:
        await update.message.reply_text(resposta_ia, parse_mode="Markdown")
    except Exception:
        await update.message.reply_text(resposta_ia)

def get_message_handler():
    return MessageHandler(filters.TEXT & (~filters.COMMAND), processar_mensagem_texto)