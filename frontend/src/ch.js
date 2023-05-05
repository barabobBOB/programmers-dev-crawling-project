import Chart from 'chart.js/auto';

const drawChart = (coinSymbol, data) => {
  const ctx = document.getElementById(`coinChart-${coinSymbol}`);
  if (!ctx) {
    return;
  }

  const chartData = {
    labels: data.map((d) => d.trade_timestamp),
    datasets: [
      {
        label: `${coinSymbol} Price`,
        data: data.map((d) => d.price),
        backgroundColor: 'rgba(78, 115, 223, 0.05)',
        borderColor: 'rgba(78, 115, 223, 1)',
        borderWidth: 1,
      },
    ],
  };

  const chartOptions = {
    scales: {
      x: {
        type: 'time',
        time: {
          unit: 'day',
        },
      },
      y: {
        ticks: {
          callback: function (value, index, values) {
            return '$' + value.toLocaleString();
          },
        },
      },
    },
  };

  new Chart(ctx, {
    type: 'line',
    data: chartData,
    options: chartOptions,
  });
};

export default drawChart;
