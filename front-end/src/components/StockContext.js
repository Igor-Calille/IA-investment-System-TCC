import React, { createContext, useState } from 'react';

export const StockContext = createContext();

export const StockProvider = ({ children }) => {
  const [selectedStocks, setSelectedStocks] = useState([]);
  const [stockData, setStockData] = useState({});

  const toggleStock = async (stockName) => {
    try {
      await fetch(`http://localhost:8000/stock-fetcher-service/add_company/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ company_symbol: stockName }), // Parâmetro no corpo
      });
      console.log(`Requisição POST para adicionar ${stockName} enviada com sucesso.`);
    } catch (error) {
      console.error(`Erro ao enviar a requisição POST para ${stockName}:`, error);
    }

    setSelectedStocks((prevSelectedStocks) =>
      prevSelectedStocks.includes(stockName)
        ? prevSelectedStocks.filter((name) => name !== stockName)
        : [...prevSelectedStocks, stockName]
    );
  };  

  const fetchStockData = async (stockName) => {
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
