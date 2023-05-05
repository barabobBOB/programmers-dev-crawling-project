import React, { useState, useEffect } from "react";
import axios from "axios";
import Chart from './ch';


const CoinList = () => {
  const [coinList, setCoinList] = useState([]);
  const [selectedCoinSymbol, setSelectedCoinSymbol] = useState(null);
  const [coinData, setCoinData] = useState([]);


  useEffect(() => {
    axios
      .post("http://127.0.0.1:8000/coin/api-v1/coinsync", {"is_sync":"True"})
      .then((response) => {
        setCoinList(response.data.coin_list);
      })
      .catch((error) => {
        console.error(error);
      });
  }, []);

  const handleCoinClick = (coinSymbol) => {
    setSelectedCoinSymbol(coinSymbol);
    axios
      .get(`http://127.0.0.1:8000/coin/api-v1/updateprice/${coinSymbol}`)
      .then((response) => {
        setCoinData(response.data);
      })
      .catch((error) => {
        console.error(error);
      });
  };

  const renderCoinList = () => {
    const columns = 3; // 한 행당 열의 개수
    const rows = Math.ceil(coinList.length / columns); // 열의 개수

    const coinBoxes = [];

    for (let i = 0; i < rows; i++) {
      const rowCoins = coinList.slice(i * columns, (i + 1) * columns);

      const coinBoxRow = rowCoins.map((coin) => (
        <div className="col-4 mb-3">
          <div className="card">
            <div className="card-body"> 
              <div className="card-title">{coin}</div>
            </div>
          </div>
        </div>
      ));

      coinBoxes.push(
        <div className="row">
          {coinBoxRow}
        </div>
      );
    }

    return coinBoxes;
  };

  const handleSync = () => {
    axios
      .get("/api/sync_coin_list")
      .then((response) => {
        setCoinList(response.data.coin_list);
      })
      .catch((error) => {
        console.error(error);
      });
  };

  return (
    <div className="col-lg-1 col-xl-4">
      <div className="card shadow mb-5" style={{ height: "415px", width: "500px" }}>
        <div className="card-header py-3 d-flex flex-row align-items-center justify-content-between">
          <h6 className="m-0 font-weight-bold text-primary">COIN LIST</h6>
          <button className="btn btn-primary" onClick={handleSync}>
            Sync
          </button>
        </div>
        <div className="card-body">
          <div className="chart-pie pt-4 pb-2">
            <div style={{ height: "300px", overflowY: "scroll" }}>
              {renderCoinList(handleCoinClick)}
            </div>
          </div>
        </div>
      </div>
      <div className="col-xl-8 col-lg-7">
        <div className="card shadow mb-4">
          <div className="card-header py-3 d-flex flex-row align-items-center justify-content-between">
            <h6 className="m-0 font-weight-bold text-primary">Coin Price Overview</h6>
            <div className="dropdown no-arrow">
              <a className="dropdown-toggle" href="#" role="button" id="dropdownMenuLink" data-toggle="dropdown"
                aria-haspopup="true" aria-expanded="false">
                <i className="fas fa-ellipsis-v fa-sm fa-fw text-gray-400"></i>
              </a>
            </div>
          </div>
          <div className="card-body">
            <div className="chart-area">
              {selectedCoinSymbol && <Chart coinSymbol={selectedCoinSymbol} coinData={coinData} />}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CoinList;

