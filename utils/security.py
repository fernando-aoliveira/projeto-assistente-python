from functools import wraps
from telegram import Update
from telegram.ext import ContextTypes
from config.settings import TELEGRAM_ADMIN_ID

def apenas_admin(func):
    """
    Decorador para restringir o uso do bot exclusivamente ao ID de administrador configurado no .env.
    """
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user_id = update.effective_user.id
        
        # Se o ADMIN_ID estiver configurado e não for o usuário atual
        if TELEGRAM_ADMIN_ID and user_id != TELEGRAM_ADMIN_ID:
            print(f"[ALERTA DE SEGURANÇA] Tentativa de acesso não autorizada pelo ID: {user_id}")
            if update.message:
                await update.message.reply_text("Acesso negado. Este assistente é privado.")
            return

        return await func(update, context, *args, **kwargs)
    return wrapper