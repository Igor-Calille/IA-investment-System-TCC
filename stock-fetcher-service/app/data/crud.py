from sqlalchemy.orm import Session
from . import models, schemas

def get_stock_data(db: Session, company_id: int):
    return db.query(models.StockData).filter(models.StockData.company_id == company_id).all()

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
