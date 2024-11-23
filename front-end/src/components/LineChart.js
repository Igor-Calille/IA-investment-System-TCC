import React from 'react';
import { Line } from 'react-chartjs-2';

const LineChart = () => {
  const data = {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    datasets: [
      {
        label: 'Revenue Stats',
        data: [30, 45, 60, 70, 90, 100, 120, 140, 160, 180, 200, 220],
        borderColor: '#42A5F5',
        fill: true,
      },
    ],
  };

  return <Line data={data} />;
};

export default LineChart;
