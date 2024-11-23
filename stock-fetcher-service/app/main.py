from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from apscheduler.schedulers.background import BackgroundScheduler
from app.data import crud, models, schemas, database
from app.services import add_company as add_company_service, update_daily_stock_data as update_daily_stock_data_service

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware
origins = [
    "http://localhost:3000",  # Origem do frontend
    "http://127.0.0.1:3000",   # Alternativa para localhost
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Permitir estas origens
    allow_credentials=True,  # Permitir cookies e autenticação
    allow_methods=["*"],  # Permitir todos os métodos HTTP
    allow_headers=["*"],  # Permitir todos os headers
)



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
        if str(e) == "Company already exists":
            raise HTTPException(status_code=200, detail="Company already exists")
        else:
            raise HTTPException(status_code=400, detail=str(e))

# Função para obter dados de ações para gráficos dinâmicos
@app.get("/stock-fetcher-service/stock-data/", response_model=List[schemas.StockData])
def get_stock_data(symbol: str, start_date: Optional[str] = Query(None), end_date: Optional[str] = Query(None), db: Session = Depends(database.get_db)):
    stock_data = crud.get_stock_data_by_symbol(db, symbol, start_date, end_date)
    if not stock_data:
        raise HTTPException(status_code=404, detail="Data not found")
    return stock_data

# Função para enviar dados das ações para treinamento de machine learning
@app.get("/stock-fetcher-service/ml-stock-data/", response_model=List[schemas.StockData])
def get_ml_stock_data(symbol: str, start_date: Optional[str] = Query(None), end_date: Optional[str] = Query(None), db: Session = Depends(database.get_db)):
    stock_data = crud.get_stock_data_by_symbol(db, symbol, start_date, end_date)
    if not stock_data:
        raise HTTPException(status_code=404, detail="Data not found")
    return stock_data
    

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
