from fastapi import FastAPI, HTTPException
import httpx

from app.services import NLPModel

app = FastAPI()

NEWS_FETCHER_SERVICE_URL = "http://news-fetcher-service:5000"	

@app.get("/sentiment-analysis-service/get_sentiment/")
async def get_sentiment(company_name: str, start_date: str = None, end_date: str = None):

    try:
        async with httpx.AsyncClient(timeout=200) as client:
            if start_date is None or end_date is None:
                response = await client.get(f"{NEWS_FETCHER_SERVICE_URL}/api/news/{company_name}/today")
            else:
                response = await client.get(f"{NEWS_FETCHER_SERVICE_URL}/api/news/{company_name}?start={start_date}&end={end_date}")
            if response.status_code == 200:
                news_data = response.json()

                nlpmodel = NLPModel()
                sentiment = nlpmodel.market_trend(news_data[0])



                return {"company_name": company_name}
            raise HTTPException(status_code=response.status_code, detail=response.text)
    except httpx.ReadTimeout:
        raise HTTPException(status_code=504, detail="Request timed out. Consider increasing the timeout value.")