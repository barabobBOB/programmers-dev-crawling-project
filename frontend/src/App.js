import React from 'react';
import CoinList from './coin_list';
import Newslist from './news_list';
import ChartComponent from './ch';
import useGetCoin from './useGetCoin';

function App() {
  const { chartData, getOneCoinData } = useGetCoin();
  return (
    <div>
      <div style={{ display: 'flex' }}>
        <ChartComponent chartData={chartData} />
        <CoinList getOneCoinData={getOneCoinData} />
      </div>
      <Newslist />
    </div>
  );
}

export default App;
