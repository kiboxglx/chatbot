from sqlalchemy import Column, Integer, String, Float, DateTime, func
from app.core.database import Base

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    amount = Column(Float)
    category = Column(String, index=True)
    date = Column(DateTime, default=func.now())
    user_phone = Column(String, index=True)
