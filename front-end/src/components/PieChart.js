import React from 'react';
import { Pie } from 'react-chartjs-2';

const PieChart = () => {
  const data = {
    labels: ['Fashion', 'Electronics', 'Health and Careness', 'Sporting Goods'],
    datasets: [
      {
        data: [33, 29, 22, 15],
        backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#FF6384'],
        hoverBackgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#FF6384'],
      },
    ],
  };

  return <Pie data={data} />;
};

export default PieChart;
