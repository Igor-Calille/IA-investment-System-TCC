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

                flattened_news_data = [item for sublist in news_data for item in sublist]

                nlpmodel = NLPModel()
                data_frame_sentiment = nlpmodel.market_trend(flattened_news_data)

                return data_frame_sentiment
            raise HTTPException(status_code=response.status_code, detail=response.text)
    except httpx.ReadTimeout:
        raise HTTPException(status_code=504, detail="Request timed out. Consider increasing the timeout value.")
    
@app.get("/sentiment-analysis-service/get_sentiment_text/")
async def get_sentiment_text(text: str):
    nlpmodel = NLPModel()
    sentiment = nlpmodel.get_text_sentiment(text)
    return sentiment