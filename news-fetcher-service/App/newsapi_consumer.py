from GoogleNews import GoogleNews
from datetime import datetime, timedelta

"""def fetch_news(start, end, company):   
    lista_noticias = []


    while start <= end:
        google_news = GoogleNews(lang='en', start='08/20/2024', end='08/29/2024', encode='utf-8')
        google_news.search(company)

        results = google_news.results()

        lista_noticias.append(results)

        start += timedelta(days=1)    

    return lista_noticias"""


def fetch_news(start, end, company):   
    lista_noticias = []

    keywords = company
    today = datetime.today()

    # Defina a data inicial para quando deseja começar a busca, por exemplo:
    start_date = start

    # Loop a cada 2 dias até o dia de hoje, garantindo que a última iteração cubra até o dia atual
    while start_date <= end:
        # Define o final do intervalo (2 dias a partir da data inicial ou até o dia de hoje, o que for menor)
        end_date = min(start_date + timedelta(days=1), end)
        
        google_news = GoogleNews(lang='en', start=start_date.strftime('%m/%d/%Y'), end=end_date.strftime('%m/%d/%Y'), encode='utf-8')
        
        # Results from news.google.com
        google_news.get_news(keywords)
        results_gnews = google_news.results()
        lista_noticias.append(results_gnews)

        # Display sorted results
        
        # Avança 2 dias
        start_date = start_date + timedelta(days=2)

    return lista_noticias