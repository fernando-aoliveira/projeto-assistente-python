import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class AIService:
    def __init__(self):
        groq_key = os.getenv("GROQ_API_KEY")
        if not groq_key:
            raise ValueError("GROQ_API_KEY não foi configurada no arquivo .env!")
            
        self.client = Groq(api_key=groq_key)
        
        self.system_instruction_base = (
            "Você é um assistente pessoal altamente eficiente, prestativo e direto ao ponto. "
            "Sua missão é ajudar o usuário no seu dia a dia com organização, dúvidas e tarefas. "
        )

        # Definição do esquema da ferramenta (Tool Spec) para a API do Groq
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "adicionar_fato_memoria",
                    "description": "Adiciona um fato ou preferência permanente importante sobre o usuário no arquivo MEMORY.md",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "categoria": {
                                "type": "string",
                                "description": "Categoria da informação (ex: Dados Pessoais, Preferências de Resposta, Projetos Atuais, Instruções Permanentes)"
                            },
                            "fato": {
                                "type": "string",
                                "description": "A informação resumida e clara a ser salva na memória permanente."
                            }
                        },
                        "required": ["categoria", "fato"]
                    }
                }
            }
        ]

    def _carregar_memoria_markdown(self) -> str:
        """Lê o arquivo MEMORY.md se ele existir na raiz do projeto."""
        caminho_memoria = "MEMORY.md"
        if os.path.exists(caminho_memoria):
            try:
                with open(caminho_memoria, "r", encoding="utf-8") as f:
                    return f.read().strip()
            except Exception as e:
                print(f"[AVISO MEMORIA] Erro ao ler MEMORY.md: {e}")
        return ""

    def _executar_adicionar_fato_memoria(self, categoria: str, fato: str) -> str:
        """
        Função Python real que abre o MEMORY.md e grava o novo fato na seção indicada.
        """
        caminho_memoria = "MEMORY.md"
        nova_linha = f"- **{fato}**\n"
        
        if not os.path.exists(caminho_memoria):
            with open(caminho_memoria, "w", encoding="utf-8") as f:
                f.write("# Memória Permanente do Assistente\n\n")

        try:
            with open(caminho_memoria, "r", encoding="utf-8") as f:
                conteudo = f.read()

            secao = f"## {categoria}"
            if secao in conteudo:
                # Insere logo abaixo do cabeçalho da seção existente
                partes = conteudo.split(secao)
                novo_conteudo = partes[0] + secao + "\n" + f"- {fato}\n" + partes[1]
            else:
                # Se a seção não existir, anexa no final do arquivo
                novo_conteudo = conteudo + f"\n\n{secao}\n- {fato}\n"

            with open(caminho_memoria, "w", encoding="utf-8") as f:
                f.write(novo_conteudo)

            print(f"[TOOL EXEC] Fato adicionado ao MEMORY.md em '{categoria}': {fato}")
            return f"Sucesso: O fato '{fato}' foi gravado na seção '{categoria}' do MEMORY.md."

        except Exception as e:
            print(f"[ERRO TOOL] Falha ao escrever no MEMORY.md: {e}")
            return f"Erro ao atualizar a memória: {e}"

    def gerar_resposta(self, historico_mensagens: list[dict]) -> str:
        """
        Gera resposta com suporte a Tool Calling para atualização de memória.
        """
        try:
            # 1. Prepara o System Prompt dinâmico com o MEMORY.md
            conteudo_memoria = self._carregar_memoria_markdown()
            system_prompt = self.system_instruction_base
            if conteudo_memoria:
                system_prompt += (
                    "\n\n==================================================\n"
                    "INFORMAÇÕES E REGRAS PERMANENTES DO USUÁRIO (MEMORY.MD):\n"
                    f"{conteudo_memoria}\n"
                    "=================================================="
                )

            # 2. Monta as mensagens
            mensagens_para_api = [{"role": "system", "content": system_prompt}]
            mensagens_para_api.extend(historico_mensagens)

            # 3. Primeira chamada à API (permite que a IA decida usar a Tool)
            completion = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=mensagens_para_api,
                tools=self.tools,
                tool_choice="auto",
                temperature=0.7,
            )

            response_message = completion.choices[0].message
            tool_calls = response_message.tool_calls

            # 4. Se a IA decidiu chamar uma ferramenta
            if tool_calls:
                # Adiciona a resposta da IA que pediu a chamada no histórico temporário da API
                mensagens_para_api.append(response_message)

                for tool_call in tool_calls:
                    if tool_call.function.name == "adicionar_fato_memoria":
                        args = json.loads(tool_call.function.arguments)
                        
                        # Executa a função Python real no servidor
                        resultado_tool = self._executar_adicionar_fato_memoria(
                            categoria=args.get("categoria", "Notas Gerais"),
                            fato=args.get("fato", "")
                        )

                        # Adiciona o resultado da execução da ferramenta para devolver à IA
                        mensagens_para_api.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": resultado_tool
                        })

                # 5. Segunda chamada à API para a IA gerar a resposta final confirmando o fato
                segunda_resposta = self.client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=mensagens_para_api
                )
                return segunda_resposta.choices[0].message.content

            # Se não usou nenhuma ferramenta, retorna a resposta de texto direta
            return response_message.content

        except Exception as e:
            print(f"[ERRO AI_SERVICE] Falha ao processar solicitação: {e}")
            return "Desculpe, tive um problema ao processar sua solicitação no momento."