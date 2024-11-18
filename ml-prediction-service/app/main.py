from fastapi import FastAPI, HTTPException
import httpx
from app.services.model import Model

app = FastAPI()

STOCK_FETCHER_SERVICE_URL = "http://stock-fetcher-service:8000"

@app.get("/ml-prediction-service/train_model/")
async def train_model(company_symbol: str, start_date: str = None, end_date: str = None):
    try:
        async with httpx.AsyncClient(timeout=200) as client:
            response = await client.get(f"{STOCK_FETCHER_SERVICE_URL}/stock-fetcher-service/ml-stock-data/?symbol={company_symbol}&start_date={start_date}&end_date={end_date}")
            if response.status_code == 200:
                # Chama o treinamento do modelo com os dados obtidos
                model = Model()
                dataframe = await model.train_model(response.json())
                
                # Retorna o resultado do modelo
                return dataframe
            raise HTTPException(status_code=response.status_code, detail=response.text)
    except httpx.ReadTimeout:
        raise HTTPException(status_code=504, detail="Request timed out. Consider increasing the timeout value.")
