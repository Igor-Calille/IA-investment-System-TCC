import React, { createContext, useState } from 'react';

export const StockContext = createContext();

export var requisicoes_enviadas = [];
export var requisicoes_finalizadas = [];

export const StockProvider = ({ children }) => {
  const [selectedStocks, setSelectedStocks] = useState([]);
  const [stockData, setStockData] = useState({});

  const toggleStock = async (stockName) => {
    setSelectedStocks((prevSelectedStocks) =>
      prevSelectedStocks.includes(stockName)
        ? prevSelectedStocks.filter((name) => name !== stockName)
        : [...prevSelectedStocks, stockName]
    );
  };  

  const fetchStockData = async (stockName) => {

    const url2 = `http://localhost:8000/stock-fetcher-service/add_company/?company_symbol=${stockName}`;
    if (!(requisicoes_enviadas.includes(stockName) || requisicoes_finalizadas.includes(stockName))) {
      try {
        requisicoes_enviadas.push(stockName);
        
        const response = await fetch(url2, {
          method: 'POST', // Define o método como POST
          headers: {
            'Content-Type': 'application/json', // Define o tipo de conteúdo como JSON
          },
          body: JSON.stringify({}), // Corpo da requisição (adicione dados aqui se necessário)
        });
        if (!response.ok) {
          throw new Error('Erro na requisição');
        }
        const result = await response.json();

        requisicoes_finalizadas.push(stockName);

      } catch (error) {
        console.error('Erro ao buscar os dados:', error);
      }
    }

    while (!requisicoes_finalizadas.includes(stockName)) {
      await new Promise((resolve) => setTimeout(resolve, 1000));
    }

    const response = await fetch(
      `http://localhost:8000/stock-fetcher-service/stock-data/?company_symbol=${stockName}&start_date=2024-06-01`
    );
    const data = await response.json();
    console.log(data);
    setStockData((prevData) => ({ ...prevData, [stockName]: data }));
  };

  return (
    <StockContext.Provider value={{ selectedStocks, toggleStock, stockData, fetchStockData }}>
      {children}
    </StockContext.Provider>
  );
};
