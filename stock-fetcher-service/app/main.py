from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
import yfinance as yf
from datetime import datetime
import pytz

app = FastAPI()

class StockHistory(BaseModel):
    date: str
    open: float
    high: float
    low: float
    close: float
    volume: int

@app.get("/stock-fetcher-service/stock-historicaldata/", response_model=List[StockHistory])
def read_stock_historicaldata(symbol: str, start_date: Optional[str] = Query(None)):
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period="max")

        if start_date:
            # Convert start_date to the same timezone as the historical data
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
            start_date_obj = pytz.timezone("America/New_York").localize(start_date_obj)
            hist = hist[hist.index >= start_date_obj]

        data = [
            {
                "date": str(date),
                "open": row["Open"],
                "high": row["High"],
                "low": row["Low"],
                "close": row["Close"],
                "volume": row["Volume"]
            }
            for date, row in hist.iterrows()
        ]
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/stock-fetcher-service/stock-lastdaydata/", response_model=StockHistory)
def read_stock_lastdaydata(symbol: str):
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period="1d")
        if not hist.empty:
            last_row = hist.iloc[-1]
            data = {
                "date": str(last_row.name),
                "open": last_row["Open"],
                "high": last_row["High"],
                "low": last_row["Low"],
                "close": last_row["Close"],
                "volume": last_row["Volume"]
            }
            return data
        else:
            raise HTTPException(status_code=404, detail="No data available for the symbol or for the last day")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        