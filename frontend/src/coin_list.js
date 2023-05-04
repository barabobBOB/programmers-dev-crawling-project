import React, { useState } from 'react';
import axios from 'axios';

function CoinList() {
  const [coinList, setCoinList] = useState([]);

  const handleResponse = () => {
    axios
      .post('http://127.0.0.1:8000/coin/api-v1/coinsync', { is_sync: 'True' })
      .then((res) => {
        const data = res.data;
        if (data.coin_list) {
          setCoinList(data.coin_list);
        } else {
          console.error('Invalid response data format: expected an object with a "coin_list" key');
        }
      })
      .catch((err) => {
        console.error(err);
      });
  };

  return (
    <div>
      <h1>Coin List</h1>
      <button onClick={handleResponse}>Response</button>
      {coinList.map((coin) => (
        <div key={coin}>
          <p>{coin}</p>
        </div>
      ))}
    </div>
  );
}

export default CoinList;
