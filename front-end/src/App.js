import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';
import Acoes from './pages/Acoes';
import Settings from './pages/Settings';
import { StockProvider } from './components/StockContext';
import './App.css';

const App = () => {
  return (
    <StockProvider>
    <Router>
      <div className="App">
        <Sidebar />
        <div className="main-content">
          <Header />
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/acoes" element={<Acoes />} />
            <Route path="/settings" element={<Settings />} />
          </Routes>
        </div>
      </div>
    </Router>
    </StockProvider>
  );
};

export default App;
