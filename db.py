from sqlalchemy import Column, Integer, String, DateTime, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

DATABASE_URL = "sqlite:///./invoices.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)  # Expense or Income name
    amount = Column(Float)
    date = Column(String)  # storing as string for simplicity (consider Date if preferred)
    type = Column(String)  # "income" or "expense"
    source_or_category = Column(String)  # source for income, category for expense
    payment_method = Column(String, nullable=True)  # only for expenses
    notes = Column(String, nullable=True)
    filename = Column(String, nullable=True)  # invoice or receipt filename
    uploaded_at = Column(DateTime, default=datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)
