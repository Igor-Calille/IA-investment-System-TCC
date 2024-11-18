from app.newsapi_consumer import fetch_news
from datetime import datetime, timedelta
from flask import Flask
from flask import request


app = Flask(__name__)

@app.route("/")
def index():
    return {"message": "Hello, World!"}

@app.route("/api/news/<company>/today")
def get_news_today(company):
    print(request.query_string)

    if request.query_string:
        return "404 Not Found", 404

    today = datetime.today()
    start = today.date() - timedelta(days=1)

    noticias = fetch_news(start, today.date(), company)

    print(noticias)

    for noticia in noticias:
        for item in noticia:
            if item['datetime'] != item['datetime']:
                item['datetime'] = None
    return noticias

@app.route("/api/news/<company>")
def get_news_range(company):

    url_params = request.args 

    if ((url_params.get('start') == "" or url_params.get('start') is None) or (url_params.get('end') == "" or url_params.get('end') is None) ):
        return "404 Not Found", 404

    try:

        start = datetime.strptime(url_params.get('start') , "%d/%m/%Y")
        end = datetime.strptime(url_params.get('end') , "%d/%m/%Y")

        if(start.date() is None or end.date() is None):
            return "404 Not Found", 404

        noticias = fetch_news(start.date(), end.date(), company)
        
        for noticia in noticias:
            for item in noticia:
                if item['datetime'] != item['datetime']:
                    item['datetime'] = None

        return noticias
    except: return "404 Not Found", 404

@app.errorhandler(404)
def not_found(error):
    return "404 Not Found", 404



