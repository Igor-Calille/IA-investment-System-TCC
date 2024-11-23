import React, { useState, useContext } from 'react';
import AcaoCard from '../components/AcaoCard';
import { StockContext } from '../components/StockContext';

const Acoes = () => {
  const { selectedStocks, toggleStock } = useContext(StockContext);
  const [searchTerm, setSearchTerm] = useState('');
  const [products, setProducts] = useState([
    { name: 'AAPL' },
    { name: 'GOOGL' },
    { name: 'AMZN' },
    { name: 'MSFT' },
    { name: 'TSLA' },
    { name: 'NFLX' },
    { name: 'NVDA' },
    { name: 'FB' },
    { name: 'BABA' },
    { name: 'V' },
    { name: 'JNJ' },
    { name: 'WMT' },
    { name: 'PG' },
    { name: 'DIS' },
    { name: 'MA' },
    { name: 'PYPL' },
    { name: 'ADBE' },
    { name: 'INTC' },
    { name: 'CSCO' },
    { name: 'ORCL' },
    { name: 'PEP' },
    { name: 'KO' },
    { name: 'CRM' },
    { name: 'NKE' },
    { name: 'MRK' },
    { name: 'MCD' },
    { name: 'COST' },
    { name: 'XOM' },
    { name: 'HON' },
    { name: 'TXN' },
    { name: 'IBM' },
    { name: 'AVGO' },
    { name: 'QCOM' },
    { name: 'LLY' },
    { name: 'T' },
    { name: 'CVX' },
    { name: 'UNH' },
    { name: 'AMGN' },
    { name: 'MDT' },
    { name: 'BA' },
    { name: 'NEE' },
    { name: 'CAT' },
    { name: 'DHR' },
    { name: 'SPGI' },
    { name: 'NOW' },
    { name: 'LIN' },
    { name: 'PLD' },
    { name: 'BLK' },
    { name: 'AXP' },
    { name: 'LOW' },
    { name: 'UPS' },
    // Adicione mais ações conhecidas aqui, se necessário
  ]);

  const handleSearch = (event) => {
    setSearchTerm(event.target.value.toUpperCase());
  };

  const handleAddProduct = (name) => {
    //if (name && name.length <= 5 && /^[A-Z]+$/.test(name) && !products.some((product) => product.name === name)) {
    setProducts([...products, { name }]);
    //}
  };

  const filteredProducts = products.filter((product) =>
    product.name.includes(searchTerm)
  );

  return (
    <div className="products-page">
      <input
        type="text"
        placeholder="Procurar por ações..."
        value={searchTerm}
        onChange={handleSearch}
        className="search-bar"
      />
      {filteredProducts.length === 0 && (
        <input
          type="text"
          placeholder="Adicionar nova ação"
          maxLength={10}
          onKeyDown={(e) => e.key === 'Enter' && handleAddProduct(e.target.value.toUpperCase())}
          className="add-product-input"
        />
      )}
      <div className="product-grid">
        {filteredProducts.map((product) => (
          <AcaoCard
            key={product.name}
            name={product.name}
            isActive={selectedStocks.includes(product.name)}
            onToggle={() => toggleStock(product.name)}
          />
        ))}
      </div>
    </div>
  );
};

export default Acoes;
