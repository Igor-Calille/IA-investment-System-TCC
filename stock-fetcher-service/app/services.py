from sqlalchemy.orm import Session
import yfinance as yf
from datetime import datetime
import pytz
from app.data import crud, schemas, models

def add_company(db: Session, company_symbol: str) -> models.Company:
    # Verifica se a empresa já existe no banco de dados
    db_company = crud.get_company_by_symbol(db, company_symbol)
    if db_company:
        raise ValueError("Company already exists")

    # Busca informações da empresa usando yfinance
    stock = yf.Ticker(company_symbol)
    company_info = stock.info

    if not company_info:
        raise ValueError("Company not found")

    # Cria um novo registro da empresa
    company_data = schemas.CompanyCreate(
        symbol=company_info.get('symbol', company_symbol),
        name=company_info.get('shortName', 'Unknown'),
        market=company_info.get('market', 'Unknown')
    )
    db_company = crud.create_company(db, company_data)

    # Busca dados históricos das ações da empresa
    hist = stock.history(period="max")
    data = [
        {
            "company_id": db_company.id,
            "date": date,
            "open": row["Open"],
            "high": row["High"],
            "low": row["Low"],
            "close": row["Close"],
            "volume": row["Volume"]
        }
        for date, row in hist.iterrows()
    ]

    # Salva os dados históricos no banco de dados
    for record in data:
        stock_data = schemas.StockDataCreate(**record)
        crud.create_stock_data(db, stock_data)

    return db_company

def update_daily_stock_data(db: Session):
    companies = crud.get_all_companies(db)
    for company in companies:
        stock = yf.Ticker(company.symbol)
        hist = stock.history(period="1d")
        if not hist.empty:
            last_row = hist.iloc[-1]
            data = {
                "company_id": company.id,
                "date": last_row.name,
                "open": last_row["Open"],
                "high": last_row["High"],
                "low": last_row["Low"],
                "close": last_row["Close"],
                "volume": last_row["Volume"]
            }
            stock_data = schemas.StockDataCreate(**data)
            crud.create_stock_data(db, stock_data)