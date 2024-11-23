import React from 'react';

const NewsItem = ({ title, subtitle, img, link, media, reporter, date }) => {
  return (
    <div className="news-item">
      <h3>{title || "Título não disponível"}</h3>
      <p>{subtitle || "Descrição não disponível"}<span> | </span><strong>{media || "Fonte desconhecida"}</strong></p>
      <p>{date || "Data não disponível"}</p>
    </div>
  );
};

export default NewsItem;
