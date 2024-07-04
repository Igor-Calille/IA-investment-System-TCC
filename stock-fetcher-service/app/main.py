from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from apscheduler.schedulers.background import BackgroundScheduler
from app.data import crud, models, schemas, database
from app.services import add_company as add_company_service, update_daily_stock_data as update_daily_stock_data_service

app = FastAPI()


# Drop existing tables
#models.Base.metadata.drop_all(bind=database.engine)

# Create tables again with updated schema
models.Base.metadata.create_all(bind=database.engine)


# Agendador para executar tarefas diárias
scheduler = BackgroundScheduler()
scheduler.start()

# Função para adicionar uma nova empresa
@app.post("/stock-fetcher-service/add_company/", response_model=schemas.Company)
def add_company(company_symbol: str = Query(...), db: Session = Depends(database.get_db)):
    try:
        db_company = add_company_service(db, company_symbol)
        return db_company
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Função para obter dados de ações para gráficos dinâmicos
@app.get("/stock-fetcher-service/stock-data/", response_model=List[schemas.StockData])
def get_stock_data(company_id: int, start_date: Optional[str] = Query(None), end_date: Optional[str] = Query(None), db: Session = Depends(database.get_db)):
    query = db.query(models.StockData).filter(models.StockData.company_id == company_id)
    if start_date:
        query = query.filter(models.StockData.date >= start_date)
    if end_date:
        query = query.filter(models.StockData.date <= end_date)
    return query.all()

# Função para enviar dados das ações para treinamento de machine learning
@app.get("/stock-fetcher-service/ml-stock-data/", response_model=List[schemas.StockData])
def get_ml_stock_data(company_id: int, db: Session = Depends(database.get_db)):
    return crud.get_stock_data(db, company_id)

# Agendamento das atualizações diárias

# Para o mercado brasileiro (B3)
@scheduler.scheduled_job('cron', hour=18, minute=0, timezone='America/Sao_Paulo')
def update_brazilian_market_data():
    db = next(database.get_db())
    update_daily_stock_data_service(db)

# Para o mercado americano (NYSE)
@scheduler.scheduled_job('cron', hour=17, minute=0, timezone='America/New_York')
def update_american_market_data():
    db = next(database.get_db())
    update_daily_stock_data_service(db)
