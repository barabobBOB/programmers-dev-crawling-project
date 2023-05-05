import React from 'react';
import ReactApexChart from 'react-apexcharts';

const ChartComponent = (chartData) => {
  class ApexChart extends React.Component {
    constructor(chartData) {
      super(chartData);

      this.state = {
        series: [
          {
            name: 'price',
            data: [10, 41, 35, 51, 49, 62, 69, 91, 148],
          },
        ],
        options: {
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
            categories: [
              'Jan',
              'Feb',
              'Mar',
              'Apr',
              'May',
              'Jun',
              'Jul',
              'Aug',
              'Sep',
            ],
          },
        },
      };
    }

    render() {
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
                    options={this.state.options}
                    series={this.state.series}
                    type="line"
                    height={350}
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      );
    }
  }

  return React.createElement(ApexChart);
};

export default ChartComponent;
