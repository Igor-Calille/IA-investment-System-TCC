import React from 'react';
import { Link } from 'react-router-dom';
import { FaTachometerAlt, FaBox, FaShoppingCart, FaWarehouse, FaUsers, FaCog, FaSignOutAlt } from 'react-icons/fa';

const Sidebar = () => {
  return (
    <aside className="sidebar">
      <ul>
        <li>
          <Link to="/" className="sidebar-button">
            <FaTachometerAlt /> Painel
          </Link>
        </li>
        <li>
          <Link to="/acoes" className="sidebar-button">
            <FaBox /> Ações
          </Link>
        </li>
        {/* <li>
          <Link to="/settings" className="sidebar-button">
            <FaCog /> Configurações
          </Link>
        </li>
        <li>
          <button className="sidebar-button">
            <FaSignOutAlt /> Logout
          </button>
        </li> */}
      </ul>
    </aside>
  );
};

export default Sidebar;
