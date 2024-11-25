from sqlalchemy.orm import Session
from . import models, schemas
from typing import List, Optional

def get_stock_data(db: Session, company_id: int):
    return db.query(models.StockData).filter(models.StockData.company_id == company_id).all()

def get_stock_data_by_symbol(db: Session, symbol: str, start_date: Optional[str] = None, end_date: Optional[str] = None) -> List[schemas.StockData]:
    # Obter o `company_id` a partir do `symbol`
    company = db.query(models.Company).filter(models.Company.symbol == symbol).first()

    if not company:
        return []

    # Realiza a consulta com join para incluir o `symbol`
    query = db.query(models.StockData, models.Company.symbol).join(models.Company, models.StockData.company_id == company.id)

    # Filtra por data se fornecido
    if start_date:
        query = query.filter(models.StockData.date >= start_date)
    if end_date:
        query = query.filter(models.StockData.date <= end_date)

    # Mapeia o resultado para incluir o campo `symbol`
    result = [
        schemas.StockData(
            company_id=stock_data.company_id,
            date=stock_data.date,
            open=stock_data.open,
            close=stock_data.close,
            low=stock_data.low,
            high=stock_data.high,
            volume=stock_data.volume,
            symbol=symbol  # Usa o símbolo do join
        )
        for stock_data, symbol in query.all()
    ]
    
    return result

def create_stock_data(db: Session, stock_data: schemas.StockDataCreate):
    db_stock_data = models.StockData(**stock_data.dict())
    db.add(db_stock_data)
    db.commit()
    db.refresh(db_stock_data)
    return db_stock_data

def create_company(db: Session, company: schemas.CompanyCreate):
    db_company = models.Company(**company.dict())
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company

def get_company_by_symbol(db: Session, symbol: str):
    return db.query(models.Company).filter(models.Company.symbol == symbol).first()

def get_company(db: Session, company_id: int):
    return db.query(models.Company).filter(models.Company.id == company_id).first()

def get_all_companies(db: Session):
    return db.query(models.Company).all()