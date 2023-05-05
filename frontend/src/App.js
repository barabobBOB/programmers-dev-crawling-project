import React from 'react';
import CoinList from './coin_list';
import Newslist from './news_list';
import ChartComponent from './ch';

function App() {
  return (
    <div>
      <div style={{ display: 'flex' }}>
        <ChartComponent />
        <CoinList />
      </div>
      <Newslist />
    </div>
  );
}

export default App;
