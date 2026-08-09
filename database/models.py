from sqlalchemy import Column, Integer, BigInteger, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database.connection import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(BigInteger, primary_key=True, index=True)  # ID numérico do Telegram
    primeiro_nome = Column(String(100), nullable=True)
    username = Column(String(100), nullable=True)
    criado_em = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relacionamento com as mensagens
    mensagens = relationship("Mensagem", back_populates="usuario", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Usuario(id={self.id}, nome='{self.primeiro_nome}')>"


class Mensagem(Base):
    __tablename__ = "mensagens"

    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(BigInteger, ForeignKey("usuarios.id"), nullable=False)
    role = Column(String(20), nullable=False)  # 'user' ou 'assistant'
    conteudo = Column(Text, nullable=False)
    criado_em = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relacionamento inverso
    usuario = relationship("Usuario", back_populates="mensagens")

    def __repr__(self):
        return f"<Mensagem(id={self.id}, role='{self.role}', usuario_id={self.usuario_id})>"