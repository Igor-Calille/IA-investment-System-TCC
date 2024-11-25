from sqlalchemy import Column, Integer, String, Float, Date, BigInteger
from .database import Base

class StockData(Base):
    __tablename__ = "stockdata"

    company_id = Column(Integer, primary_key=True)
    date = Column(Date, primary_key=True)
    open = Column(Float)
    close = Column(Float)
    low = Column(Float)
    high = Column(Float)
    volume = Column(BigInteger)  # Update this line

class Company(Base):
    __tablename__ = "company"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, index=True)
    name = Column(String)
    market = Column(String)