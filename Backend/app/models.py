from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class ChatHistory(Base):
    __tablename__ = 'chat_history'
    id = Column(Integer, primary_key=True)  
    chatId = Column(Integer, index=True)
    prompt = Column(String)
    completion = Column(String)
    time = Column(DateTime, default=datetime.utcnow)

engine = create_engine('sqlite:///./test.db', echo=True)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
