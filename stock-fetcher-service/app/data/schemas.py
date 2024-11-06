from pydantic import BaseModel
from datetime import date

class StockDataBase(BaseModel):
    company_id: int
    date: date
    open: float
    close: float
    low: float
    high: float
    volume: int

class StockDataCreate(StockDataBase):
    pass

class StockData(StockDataBase):

    symbol:str

    class Config:
        orm_mode = True

class CompanyBase(BaseModel):
    symbol: str
    name: str
    market: str

class CompanyCreate(CompanyBase):
    pass

class Company(CompanyBase):
    id: int

    class Config:
        orm_mode = True
