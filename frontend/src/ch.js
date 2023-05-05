import React, { useEffect, useState } from 'react';
import ReactApexChart from 'react-apexcharts';

const ChartComponent = ({ chartData }) => {
  const [options, setOptions] = useState({
    chart: {
      height: 350,
      type: 'line',
      zoom: {
        enabled: false,
      },
    },
    dataLabels: {
      enabled: false,
    },
    stroke: {
      curve: 'straight',
    },
    title: {
      text: 'Product Trends by Month',
      align: 'left',
    },
    grid: {
      row: {
        colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
        opacity: 0.5,
      },
    },
    xaxis: {
      categories: [],
    },
  });

  const [series, setSeries] = useState([
    {
      name: '',
      data: [],
    },
  ]);

  useEffect(() => {
    if (chartData.length > 0) {
      const categories = chartData.map((data) => data.trade_timestamp);
      const seriesData = chartData.map((data) => data.price);
      setOptions({
        ...options,
        xaxis: {
          categories: categories,
        },
      });
      setSeries([
        {
          name: chartData[0].coin_symbol,
          data: seriesData,
        },
      ]);
    }
  }, [chartData, options]);

  if (chartData.data && chartData.data.length === 0) {
    return null;
  }

  return (
    <div className="col-xl-7 col-lg-8">
      <div className="card shadow mb-4">
        <div className="card-header py-3 d-flex flex-row align-items-center justify-content-between">
          <h6 className="m-0 font-weight-bold text-primary">
            Earnings Overview
          </h6>
          <div className="dropdown no-arrow"></div>
        </div>

        <div className="card-body">
          <div className="chart-area">
            <div id="chart">
              <ReactApexChart
                options={options}
                series={series}
                type="line"
                height={350}
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChartComponent;
