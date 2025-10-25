import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Bar } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const BarChart = ({ 
  data, 
  title, 
  color = '#007bff', 
  height = 200,
  showLegend = false,
  horizontal = false 
}) => {
  const chartData = {
    labels: data.map(item => item.label),
    datasets: [
      {
        label: title,
        data: data.map(item => item.value),
        backgroundColor: color,
        borderColor: color,
        borderWidth: 1,
        borderRadius: 4,
        borderSkipped: false,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    indexAxis: horizontal ? 'y' : 'x',
    plugins: {
      legend: {
        display: showLegend,
        position: 'top',
      },
      title: {
        display: false,
      },
      tooltip: {
        backgroundColor: 'rgba(0, 0, 0, 0.8)',
        titleColor: '#fff',
        bodyColor: '#fff',
        borderColor: color,
        borderWidth: 1,
      },
    },
    scales: {
      x: {
        grid: {
          display: false,
        },
        ticks: {
          color: '#666',
          font: {
            size: 12,
          },
        },
      },
      y: {
        grid: {
          color: '#f0f0f0',
        },
        ticks: {
          color: '#666',
          font: {
            size: 12,
          },
        },
      },
    },
  };

  return (
    <div style={{ height: `${height}px`, width: '100%' }}>
      <Bar data={chartData} options={options} />
    </div>
  );
};

export default BarChart;
