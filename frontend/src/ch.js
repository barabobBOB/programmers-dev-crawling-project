import React, { useState, useEffect } from "react";
import axios from "axios";
import Chart from "chart.js";

const CoinChart = ({ coinSymbol }) => {
  const [priceData, setPriceData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(
          `http://127.0.0.1:8000/coin/api-v1/updateprice/${coinSymbol}`
        );
        setPriceData(response.data);
      } catch (error) {
        console.error(error);
      }
    };

    fetchData();
  }, [coinSymbol]);

  useEffect(() => {
    if (priceData.length === 0) {
      return;
    }

    const ctx = document.getElementById(`coin-chart-${coinSymbol}`).getContext("2d");

    const data = {
      labels: priceData.map((data) => data.trade_timestamp),
      datasets: [
        {
          label: `Price of ${coinSymbol}`,
          data: priceData.map((data) => data.price),
          backgroundColor: "rgba(75, 192, 192, 0.2)",
          borderColor: "rgba(75, 192, 192, 1)",
          borderWidth: 1,
        },
      ],
    };

    const options = {
      scales: {
        xAxes: [
          {
            type: "time",
            time: {
              unit: "day",
              displayFormats: {
                day: "MMM DD",
              },
            },
            ticks: {
              source: "labels",
            },
          },
        ],
      },
    };

    new Chart(ctx, {
      type: "line",
      data: data,
      options: options,
    });
  }, [priceData, coinSymbol]);

  return (
    <div className="card shadow mb-4">
      <div className="card-header py-3">
        <h6 className="m-0 font-weight-bold text-primary">{coinSymbol} Price Overview</h6>
      </div>
      <div className="card-body">
        <div className="chart-area">
          <canvas id={`coin-chart-${coinSymbol}`}></canvas>
        </div>
      </div>
    </div>
  );
};

export default CoinChart;
