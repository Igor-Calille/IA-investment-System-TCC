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
    { name: 'FB' }
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
