from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import httpx
from typing import List, Optional
import json

app = FastAPI()

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

# Serviço stock-fetcher-service
STOCK_FETCHER_SERVICE_URL = "http://stock-fetcher-service:8000"

@app.post("/stock-fetcher-service/add_company/")
async def add_company(company_symbol: str):
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(f"{STOCK_FETCHER_SERVICE_URL}/stock-fetcher-service/add_company/?company_symbol={company_symbol}")
            if response.status_code == 200:
                return response.json()
            # Adiciona mensagem de erro mais clara
            raise HTTPException(
                status_code=response.status_code, 
                detail=f"Erro do serviço interno: {response.text}"
            )
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Erro ao processar a requisição: {str(e)}"
        )


@app.get("/stock-fetcher-service/stock-data/", response_model=List[dict])
async def get_stock_data(company_symbol: str, start_date: Optional[str] = Query(None), end_date: Optional[str] = Query(None)):
    params = {"symbol": company_symbol, "start_date": start_date, "end_date": end_date}
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{STOCK_FETCHER_SERVICE_URL}/stock-fetcher-service/stock-data/", params=params)
        if response.status_code == 200:
            return response.json()
        raise HTTPException(status_code=response.status_code, detail=response.text)

@app.get("/stock-fetcher-service/ml-stock-data/", response_model=List[dict])
async def get_ml_stock_data(company_symbol: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{STOCK_FETCHER_SERVICE_URL}/stock-fetcher-service/ml-stock-data/", params={"symbol": company_symbol})
        if response.status_code == 200:
            return response.json()
        raise HTTPException(status_code=response.status_code, detail=response.text)
    
# Serviço ml-prediction-service
ML_PREDICTION_SERVICE_URL = "http://ml-prediction-service:8000"

@app.get("/ml-prediction-service/train_model/")
async def train_model(company_symbol: str, start_date: Optional[str] = Query(None), end_date: Optional[str] = Query(None)):
    async with httpx.AsyncClient(timeout=210) as client:
        response = await client.get(f"{ML_PREDICTION_SERVICE_URL}/ml-prediction-service/train_model/?company_symbol={company_symbol}&start_date={start_date}&end_date={end_date}")
        
        if response.status_code == 200:
            response_json = response.json()

            # Salva o JSON em um arquivo
            file_path = f"{company_symbol}_train_model_data.json"
            with open(file_path, "w") as file:
                json.dump(response_json, file)

            print(f"JSON saved to {file_path}")
            return response_json
        raise HTTPException(status_code=response.status_code, detail=response.text)
    
@app.get("/news-fetcher-service/news/today/")
async def get_news_today(company: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://news-fetcher-service:5000/api/news/{company}/today")
        if response.status_code == 200:
            return response.json()
        raise HTTPException(status_code=response.status_code, detail=response.text)
    
@app.get("/news-fetcher-service/news/by_date/")
async def get_news_today(company: str, start_date: str, end_date: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://news-fetcher-service:5000/api/news/{company}?start={start_date}&end={end_date}")
        if response.status_code == 200:
            return response.json()
        raise HTTPException(status_code=response.status_code, detail=response.text)
    
# Obter a media do sentimento entre as noticias de cada dia de um intervalo de datas
@app.get("/sentiment-analysis-service/get_sentiment/")
async def get_sentiment(company_name: str, start_date: str = None, end_date: str = None):
    
    async with httpx.AsyncClient(timeout=200) as client:
        response = await client.get(f"http://sentiment-analysis-service:8000/sentiment-analysis-service/get_sentiment/?company_name={company_name}&start_date={start_date}&end_date={end_date}")
        if response.status_code == 200:
            return response.json()
        raise HTTPException(status_code=response.status_code, detail=response.text)
    
# Obter o sentimento de um texto
@app.get("/sentiment-analysis-service/get_sentiment_text/")
async def get_sentiment(text: str):
    
    async with httpx.AsyncClient(timeout=200) as client:
        response = await client.get(f"http://sentiment-analysis-service:8000/sentiment-analysis-service/get_sentiment_text/?text={text}")
        if response.status_code == 200:
            return response.json()
        raise HTTPException(status_code=response.status_code, detail=response.text)

    