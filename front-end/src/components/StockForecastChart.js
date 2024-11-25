import React, { useState, useEffect } from 'react';
import ApexCharts from 'react-apexcharts';
import { requisicoes_enviadas, requisicoes_finalizadas } from '../components/StockContext';

const StockForecastChart = ({ stock }) => {
  const [chartData, setChartData] = useState([]);
  const [predictedData, setPredictedData] = useState([]);
  const [loading, setLoading] = useState(true); // Adiciona estado de carregamento

  useEffect(() => {
    const url = `http://localhost:8000/ml-prediction-service/train_model/?company_symbol=${stock}&start_date="2024-01-09"&end_date="2024-12-31"`;

    const fetchData = async () => {
      try {
        // const url2 = `http://localhost:8000/stock-fetcher-service/add_company/?company_symbol=${stock}`;
        // if (!(requisicoes_enviadas.includes(stock) || requisicoes_finalizadas.includes(stock))) {
        //   try {
        //     requisicoes_enviadas.push(stock);

        //     const response = await fetch(url2, {
        //       method: 'POST',
        //       headers: {
        //         'Content-Type': 'application/json',
        //       },
        //       body: JSON.stringify({}),
        //     });
        //     if (!response.ok) {
        //       throw new Error('Erro na requisição');
        //     }
        //     await response.json();
        //     requisicoes_finalizadas.push(stock);
        //   } catch (error) {
        //     console.error('Erro ao buscar os dados:', error);
        //   }
        // }

        while (!requisicoes_finalizadas.includes(stock)) {
          await new Promise((resolve) => setTimeout(resolve, 1000));
        }

        const response = await fetch(url);
        if (!response.ok) {
          throw new Error('Erro na requisição');
        }
        const result = await response.json();

        console.log('Resultado da previsão:', result);

        const filteredData = Array.from(
          new Map(result.data.map((item) => [item.date, item])).values()
        );

        const sortedData = filteredData.sort((a, b) => new Date(a.date) - new Date(b.date));

        sortedData.pop();

        const formattedData = sortedData.map((item) => ({
          x: new Date(item.date),
          y: item.close,
        }));

        const formattedPredictedData = sortedData.map((item) => ({
          x: new Date(item.date),
          y: item.predicted_close,
        }));

        setChartData(formattedData);
        setPredictedData(formattedPredictedData);
      } catch (error) {
        console.error('Erro ao buscar os dados:', error);
      } finally {
        setLoading(false); // Define carregamento como concluído
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
      {loading ? ( // Verifica se os dados ainda estão carregando
        <div className="loading-box">
          <p>Carregando Dados...</p>
        </div>
      ) : (
        <ApexCharts options={options} series={series} type="line" height={350} width="100%" />
      )}
    </div>
  );
};

export default StockForecastChart;