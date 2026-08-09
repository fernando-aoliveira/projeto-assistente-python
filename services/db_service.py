from sqlalchemy.orm import Session
from database.connection import SessionLocal
from database.models import Usuario, Mensagem

class DBService:
    @staticmethod
    def salvar_ou_atualizar_usuario(user_id: int, primeiro_nome: str, username: str = None):
        """Garante que o usuário esteja cadastrado na tabela 'usuarios'."""
        db: Session = SessionLocal()
        try:
            usuario = db.query(Usuario).filter(Usuario.id == user_id).first()
            if not usuario:
                usuario = Usuario(id=user_id, primeiro_nome=primeiro_nome, username=username)
                db.add(usuario)
            else:
                usuario.primeiro_nome = primeiro_nome
                usuario.username = username
            db.commit()
        except Exception as e:
            db.rollback()
            print(f"[ERRO BANCO] Falha ao salvar usuário: {e}")
        finally:
            db.close()

    @staticmethod
    def salvar_mensagem(user_id: int, role: str, conteudo: str):
        """Salva uma nova mensagem (do usuário ou da IA) na tabela 'mensagens'."""
        db: Session = SessionLocal()
        try:
            nova_msg = Mensagem(usuario_id=user_id, role=role, conteudo=conteudo)
            db.add(nova_msg)
            db.commit()
        except Exception as e:
            db.rollback()
            print(f"[ERRO BANCO] Falha ao salvar mensagem: {e}")
        finally:
            db.close()

    @staticmethod
    def obter_historico_recente(user_id: int, limite: int = 10) -> list[dict]:
        """
        Busca as últimas 'limite' mensagens do usuário no banco de dados
        e retorna no formato exigido pela API do Groq/Llama.
        """
        db: Session = SessionLocal()
        try:
            # Busca as N mensagens mais recentes ordenadas por id decrescente
            mensagens = (
                db.query(Mensagem)
                .filter(Mensagem.usuario_id == user_id)
                .order_by(Mensagem.id.desc())
                .limit(limite)
                .all()
            )
            
            # Inverte para manter a ordem cronológica (mais antiga -> mais recente)
            mensagens.reverse()
            
            # Formata para a lista de dicionários exigida pela IA
            return [{"role": msg.role, "content": msg.conteudo} for msg in mensagens]
        except Exception as e:
            print(f"[ERRO BANCO] Falha ao carregar histórico: {e}")
            return []
        finally:
            db.close()