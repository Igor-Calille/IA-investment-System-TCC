import React, { useState, useEffect } from 'react';
import ApexCharts from 'react-apexcharts';
import { requisicoes_enviadas, requisicoes_finalizadas } from '../components/StockContext';

const StockChart = ({ stock, data }) => {
  const [chartData, setChartData] = useState([]);

  useEffect(() => {
    if (data) {
      if (Array.isArray(data)) {
        // Formatar os dados no formato que o ApexCharts espera
        const formattedData = data.map((item) => ({
          x: new Date(item.date),
          y: [item.open.toFixed(2), item.high.toFixed(2), item.low.toFixed(2), item.close.toFixed(2)],
        }));
        setChartData(formattedData);
      }
    }
  }, [data]);

  const options = {
    chart: {
      type: 'candlestick',
      height: 350,
    },
    title: {
      text: `Ação: ${stock}`,
      align: 'left',
    },
    xaxis: {
      type: 'datetime',
      labels: {
        formatter: function (value) {
          const date = new Date(value);
          return `${date.getDate().toString().padStart(2, '0')}/${(date.getMonth() + 1)
            .toString()
            .padStart(2, '0')}`;
        },
      },
    },
    yaxis: {
      tooltip: {
        enabled: true,
      },
      labels: {
        formatter: function (value) {
          return value.toFixed(0); // Formata para uma casa decimal
        },
      },
    },
  };

  const series = [
    {
      data: chartData,
    },
  ];

  return (
    <div className="stock-chart-container">
      {chartData.length === 0 ? ( // Verifica se os dados ainda estão carregando
        <div className="loading-box">
          <p>Carregando Dados...</p>
        </div>
      ) : (
        <ApexCharts options={options} series={series} type="candlestick" height={350} width="100%" />
      )}
    </div>
  );
};

export default StockChart;
