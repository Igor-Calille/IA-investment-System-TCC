import React from 'react';

const AcaoCard = ({ name, isActive, onToggle }) => {
  return (
    <div className="product-card">
      <button className="product-name">{name}</button>
      <label className="toggle-switch">
        <input type="checkbox" checked={isActive} onChange={onToggle} />
        <span className="slider"></span>
      </label>
    </div>
  );
};

export default AcaoCard;
