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

STOCK_FETCHER_URL = "http://stock-fetcher-service:8000"

@app.get("/stocks/")
async def get_stocks(symbol: str, start_date: Optional[str] = Query(None)):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{STOCK_FETCHER_URL}/stocks/?symbol={symbol}&start_date={start_date}")
        if response.status_code == 200:
            return response.json()
        raise HTTPException(status_code=response.status_code, detail=response.text)
