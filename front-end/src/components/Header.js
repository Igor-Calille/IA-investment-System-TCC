import React from 'react';
import { FaUserCircle } from 'react-icons/fa';

const Header = () => {
  return (
    <header className="header">
      <h1>Bem vindo de volta, Usuario</h1>
      <p>TCC</p>
      <div className="header-right">
        <FaUserCircle size={30} />
        <span>Nome Usuario</span>
      </div>
    </header>
  );
};

export default Header;
