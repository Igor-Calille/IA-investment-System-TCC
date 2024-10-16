from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import httpx
from typing import List, Optional

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
async def get_stock_data(company_id: int, start_date: Optional[str] = Query(None), end_date: Optional[str] = Query(None)):
    params = {"company_id": company_id, "start_date": start_date, "end_date": end_date}
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{STOCK_FETCHER_SERVICE_URL}/stock-fetcher-service/stock-data/", params=params)
        if response.status_code == 200:
            return response.json()
        raise HTTPException(status_code=response.status_code, detail=response.text)

@app.get("/stock-fetcher-service/ml-stock-data/", response_model=List[dict])
async def get_ml_stock_data(company_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{STOCK_FETCHER_SERVICE_URL}/stock-fetcher-service/ml-stock-data/", params={"company_id": company_id})
        if response.status_code == 200:
            return response.json()
        raise HTTPException(status_code=response.status_code, detail=response.text)
    




@app.get("/news-fetcher-service/")
