import React from 'react';
import { Line } from 'react-chartjs-2';

const StockPriceChart = () => {
  const data = {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    datasets: [
      {
        label: 'Stock Price',
        data: [150, 160, 155, 165, 170, 175, 180, 185, 190, 195, 200, 210],
        borderColor: '#4caf50',
        fill: false,
      },
    ],
  };

  return <Line data={data} />;
};

export default StockPriceChart;
