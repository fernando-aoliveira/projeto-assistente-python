import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class AIService:
    def __init__(self):
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

    def gerar_resposta(self, historico_mensagens: list[dict]) -> str:
        """
        Recebe a lista de histórico (System Prompt + Histórico do DB + Mensagem Atual)
        e gera a resposta usando a IA.
        """
        try:
            # Monta o payload final: System Prompt + Histórico do Banco de Dados
            mensagens_para_api = [{"role": "system", "content": self.system_instruction}]
            mensagens_para_api.extend(historico_mensagens)

            completion = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=mensagens_para_api,
                temperature=0.7,
            )
            return completion.choices[0].message.content
        except Exception as e:
            print(f"[ERRO AI_SERVICE] Falha ao chamar a API: {e}")
            return "Desculpe, tive um problema ao processar sua solicitação com a IA no momento."