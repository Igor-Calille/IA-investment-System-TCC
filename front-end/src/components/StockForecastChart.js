import React, { useState, useEffect } from 'react';
import ApexCharts from 'react-apexcharts';

const StockForecastChart = ({ stock }) => {
  const [chartData, setChartData] = useState([]);
  const [predictedData, setPredictedData] = useState([]);

  useEffect(() => {
    const url = `http://localhost:8000/ml-prediction-service/train_model/?company_symbol=${stock}&start_date="2024-01-09"&end_date="2024-12-31"`;
  
    const fetchData = async () => {
      try {
        const response = await fetch(url);
        if (!response.ok) {
          throw new Error('Erro na requisição');
        }
        const result = await response.json();
  
        console.log('Resultado da previsão:', result);
  
        // Remover duplicatas baseadas na data
        const filteredData = Array.from(
          new Map(result.data.map((item) => [item.date, item])).values()
        );
  
        // Ordenar por data (menor para maior)
        const sortedData = filteredData.sort((a, b) => new Date(a.date) - new Date(b.date));

        // Remover o ultimo elemento (previsão)
        sortedData.pop();
  
        // Formatar os dados de fechamento
        const formattedData = sortedData.map((item) => ({
          x: new Date(item.date),
          y: item.close,
        }));
  
        // Formatar os dados de previsão
        const formattedPredictedData = sortedData.map((item) => ({
          x: new Date(item.date),
          y: item.predicted_close,
        }));
  
        setChartData(formattedData);
        setPredictedData(formattedPredictedData);
      } catch (error) {
        console.error('Erro ao buscar os dados:', error);
      }
    };
  
    fetchData();
  }, [stock]);
  

  const options = {
    chart: {
      type: 'line',
      height: 350,
    },
    stroke: {
      width: 2,
      curve: 'smooth',
    },
    title: {
      text: `Previsão para: ${stock}`,
      align: 'left',
    },
    xaxis: {
      type: 'datetime',
      labels: {
        formatter: function (value) {
          const date = new Date(value);
          return `${date.getDate().toString().padStart(2, '0')}/${(date.getMonth() + 1).toString().padStart(2, '0')}`;
        }
      }
    },
    yaxis: {
      tooltip: {
        enabled: true,
      },
      labels: {
        formatter: function (value) {
          return value.toFixed(2);
        },
      },
    },
  };

  const series = [
    {
      name: 'Fechamento Real',
      data: chartData,
    },
    {
      name: 'Previsão (Predicted Close)',
      data: predictedData,
    },
  ];

  return (
    <div className="forecast-chart-container">
      <ApexCharts options={options} series={series} type="line" height={350} width="100%" />
    </div>
  );
};

export default StockForecastChart;
