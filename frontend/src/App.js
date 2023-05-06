import React, { useState } from 'react';
import CoinList from './coin_list';
import Newslist from './news_list';
import ChartComponent from './ch';
import { getOneCoinData } from './useGetCoin';
import UseGetSymbolNews from './symbolNews';

function App() {
  const [ chartData, setChartData ] = useState([]);
  const [ clickedSymbol, setClickedSymbol ] = useState('');

  const onClick = async(coinSymbol) => {
    const response = await getOneCoinData(coinSymbol);
    setChartData(response);
  }

  return (
    <div>
      <div style={{ display: 'flex' }}>
        <ChartComponent chartData={chartData} />
        <CoinList getOneCoinData={onClick} setClickedSymbol={setClickedSymbol} />
      </div>
      <UseGetSymbolNews coinSymbol={clickedSymbol}/>
      <Newslist />
    </div>
  );
}

export default App;
