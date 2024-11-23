import React, { useContext, useEffect, useState } from 'react';
import { StockContext } from '../components/StockContext';
import StockChart from '../components/StockChart';
import StockForecastChart from '../components/StockForecastChart';
import NewsItem from '../components/NewsItem';
import TradeDecisionBox from '../components/TradeDecisionBox'; // Importar o componente

const Dashboard = () => {
  const { selectedStocks, fetchStockData, stockData } = useContext(StockContext);
  const [newsData, setNewsData] = useState({});

  useEffect(() => {
    selectedStocks.forEach((stock) => {
      fetchStockData(stock);

      // Tentar carregar notícias do cache (localStorage)
      const cachedNews = localStorage.getItem(`news_${stock}`);
      const cachedData = cachedNews ? JSON.parse(cachedNews) : null;

      // Verifica se existe cache e se é recente (ex.: menos de 1 dia)
      const isCacheValid = cachedData && (Date.now() - cachedData.timestamp < 24 * 60 * 60 * 1000);

      if (isCacheValid) {
        setNewsData((prevData) => ({
          ...prevData,
          [stock]: cachedData.news,
        }));
      } else {
        fetch(`http://localhost:8000/news-fetcher-service/news/today/?company=${stock}`)
          .then((response) => response.json())
          .then((news) => {
            console.log('Notícias:', news);
            const sortedNews = news[0]
              .sort((a, b) => new Date(b.datetime) - new Date(a.datetime))
              .slice(0, 3);

            setNewsData((prevData) => ({
              ...prevData,
              [stock]: sortedNews,
            }));

            localStorage.setItem(
              `news_${stock}`,
              JSON.stringify({ news: sortedNews, timestamp: Date.now() })
            );
          })
          .catch((error) => console.error(`Erro ao buscar notícias para ${stock}:`, error));
      }
    });
  }, [selectedStocks]);

  return (
    <div className="dashboard">
      <h1>Suas ações</h1>
      <div className="charts-grid">
        {selectedStocks.length === 0 ? (
          <p>Nenhuma ação selecionada</p>
        ) : (
          selectedStocks.map((stock) => (
            <div key={stock} className="stock-section">
              <div className="stock-charts-container">
                <StockChart stock={stock} data={stockData[stock]} />
                <StockForecastChart stock={stock} data={stockData[stock]} />
              </div>
              <TradeDecisionBox stock={stock} />
              <div className="news-section">
                <h2>Notícias Relevantes</h2>
                {newsData[stock] &&
                  newsData[stock].map((news, index) => (
                    <NewsItem
                      key={index}
                      title={news.title}
                      subtitle={news.desc}
                      media={news.media}
                      date={news.date}
                    />
                  ))}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default Dashboard;