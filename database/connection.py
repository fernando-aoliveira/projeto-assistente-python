from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config.settings import DATABASE_URL

# Cria o engine de conexão
engine = create_engine(DATABASE_URL, echo=False)

# Criador de sessões para executar queries
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe base para a criação dos Modelos (Tabelas)
Base = declarative_base()

def get_db():
    """Gera e fecha uma sessão do banco de dados com segurança."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Cria todas as tabelas no PostgreSQL se elas ainda não existirem."""
    from database import models  # Importa os modelos para registrá-los na Base
    Base.metadata.create_all(bind=engine)
    print("[BANCO DE DADOS] Tabelas verificadas/criadas com sucesso no PostgreSQL!")