import os
from collections import deque
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class AIService:
    def __init__(self, limite_historico: int = 10):
        groq_key = os.getenv("GROQ_API_KEY")
        if not groq_key:
            raise ValueError("GROQ_API_KEY não foi configurada no arquivo .env!")
            
        self.client = Groq(api_key=groq_key)
        
        self.system_instruction = (
            "Você é um assistente pessoal altamente eficiente, prestativo e direto ao ponto. "
            "Sua missão é ajudar o usuário no seu dia a dia com organização, dúvidas e tarefas. "
            "Responda sempre em português do Brasil de forma concisa e amigável, "
            "utilizando formatação Markdown quando adequado para facilitar a leitura."
        )
        
        # Mantém até 'limite_historico' mensagens recentes na memória (curto prazo)
        self.historico = deque(maxlen=limite_historico)

    def gerar_resposta(self, mensagem_usuario: str) -> str:
        """Envia o histórico recente e a nova mensagem do usuário para a IA."""
        try:
            # 1. Adiciona a nova mensagem do usuário ao histórico
            self.historico.append({"role": "user", "content": mensagem_usuario})

            # 2. Monta a lista completa de mensagens enviadas para a API (System Prompt + Histórico)
            mensagens_para_api = [{"role": "system", "content": self.system_instruction}]
            mensagens_para_api.extend(list(self.historico))

            # 3. Chama a API do Groq
            completion = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=mensagens_para_api,
                temperature=0.7,
            )
            
            resposta_ia = completion.choices[0].message.content

            # 4. Adiciona a resposta da IA ao histórico de contexto
            self.historico.append({"role": "assistant", "content": resposta_ia})

            return resposta_ia

        except Exception as e:
            print(f"[ERRO AI_SERVICE - GROQ] Falha ao chamar a API: {e}")
            return "Desculpe, tive um problema ao processar sua solicitação com a IA no momento."