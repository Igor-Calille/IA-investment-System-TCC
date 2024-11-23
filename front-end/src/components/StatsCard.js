import React from 'react';

const StatsCard = ({ title, value, percentage, description }) => {
  return (
    <div className="stats-card">
      <h3>{title}</h3>
      <p>{value}</p>
      <span>{percentage}</span>
      <small>{description}</small>
    </div>
  );
};

export default StatsCard;
