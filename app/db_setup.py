from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DB_URL = "sqlite:///./chat_data.db"

engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
SessionMaker = sessionmaker(bind=engine, expire_on_commit=False)
Base = declarative_base()

def init_db():
    import app.models
    Base.metadata.create_all(bind=engine)