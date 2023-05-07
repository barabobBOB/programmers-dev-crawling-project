import React, { useEffect, useState } from 'react';
import ReactApexChart from 'react-apexcharts';
import axios from 'axios';

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

  const [selectedYear, setSelectedYear] = useState(new Date().getFullYear());

  useEffect(() => {
    if (chartData.length === 0) return;
    if (chartData.length > 0) {
      const filteredData = chartData.filter(
        (data) => new Date(data.trade_timestamp).getFullYear() === selectedYear,
      );
      if (filteredData.length > 0) {
        const categories = filteredData.map((data) => data.trade_timestamp);
        const seriesData = filteredData.map((data) => data.price);
        setOptions({
          ...options,
          xaxis: {
            categories: categories,
          },
        });
        setSeries([
          {
            name: filteredData[0].coin_symbol,
            data: seriesData,
          },
        ]);
      }
    }
  }, [chartData, selectedYear, setOptions, setSeries]);

  return (
    <div className="col-xl-7 col-lg-8">
      <div className="card shadow mb-4">
        <div className="card-header py-3 d-flex flex-row align-items-center justify-content-between">
          <h6 className="m-0 font-weight-bold text-primary">
            Earnings Overview
          </h6>
          <div className="dropdown no-arrow">
            <select
              value={selectedYear}
              onChange={(e) => setSelectedYear(parseInt(e.target.value))}
            >
              <option value={new Date().getFullYear()}>This year</option>
              <option value={new Date().getFullYear() - 1}>Last year</option>
              <option value={new Date().getFullYear() - 2}>
                {new Date().getFullYear() - 2}
              </option>
              <option value={new Date().getFullYear() - 3}>
                {new Date().getFullYear() - 3}
              </option>
              <option value={new Date().getFullYear() - 4}>
                {new Date().getFullYear() - 4}
              </option>
            </select>
          </div>
        </div>

        <div className="card-body">
          <div className="chart-area">
            <div id="chart">
              {chartData.length > 0 ? (
                <ReactApexChart
                  options={options}
                  series={series}
                  type="line"
                  height={350}
                />
              ) : (
                <p>No data available for selected year.</p>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChartComponent;
