from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import httpx
from typing import List, Optional
import json

app = FastAPI()

origins = [
    "http://localhost:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serviço stock-fetcher-service
STOCK_FETCHER_SERVICE_URL = "http://stock-fetcher-service:8000"

@app.post("/stock-fetcher-service/add_company/")
async def add_company(company_symbol: str):
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(f"{STOCK_FETCHER_SERVICE_URL}/stock-fetcher-service/add_company/?company_symbol={company_symbol}")
        if response.status_code == 200:
            return response.json()
        raise HTTPException(status_code=response.status_code, detail=response.text)

@app.get("/stock-fetcher-service/stock-data/", response_model=List[dict])
async def get_stock_data(symbol: str, start_date: Optional[str] = Query(None), end_date: Optional[str] = Query(None)):
    params = {"symbol": symbol, "start_date": start_date, "end_date": end_date}
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{STOCK_FETCHER_SERVICE_URL}/stock-fetcher-service/stock-data/", params=params)
        if response.status_code == 200:
            return response.json()
        raise HTTPException(status_code=response.status_code, detail=response.text)

@app.get("/stock-fetcher-service/ml-stock-data/", response_model=List[dict])
async def get_ml_stock_data(symbol: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{STOCK_FETCHER_SERVICE_URL}/stock-fetcher-service/ml-stock-data/", params={"symbol": symbol})
        if response.status_code == 200:
            return response.json()
        raise HTTPException(status_code=response.status_code, detail=response.text)
    
# Serviço ml-prediction-service
ML_PREDICTION_SERVICE_URL = "http://ml-prediction-service:8000"

@app.get("/ml-prediction-service/train_model/")
async def train_model(company_symbol: str, start_date: Optional[str] = Query(None), end_date: Optional[str] = Query(None)):
    async with httpx.AsyncClient(timeout=210) as client:
        response = await client.get(f"{ML_PREDICTION_SERVICE_URL}/ml-prediction-service/train_model/?company_symbol={company_symbol}&start_date={start_date}")
        
        if response.status_code == 200:
            response_json = response.json()

            # Salva o JSON em um arquivo
            file_path = f"{company_symbol}_train_model_data.json"
            with open(file_path, "w") as file:
                json.dump(response_json, file)

            print(f"JSON saved to {file_path}")
            return response_json
        raise HTTPException(status_code=response.status_code, detail=response.text)

    