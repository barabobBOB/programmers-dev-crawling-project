// import { useState, useEffect } from 'react';
// import axios from 'axios';

// function CoinList() {
//   const [coinList, setCoinList] = useState([]);
//   const [coinPriceList, setCoinPriceList] = useState([]);
//   const [loading, setLoading] = useState(false);

//   useEffect(() => {
//     async function fetchCoinList() {
//       try {
//         const response = await axios.post('http://127.0.0.1:8000/coin/api-v1/coinsync', {"is_sync": "True"});
//         setCoinList(response.data.coin_list);
//       } catch (error) {
//         console.error(error);
//       }
//     }
//     fetchCoinList();
//   }, []);

//   async function fetchCoinPrice(coinSymbol) {
//     try {
//       const response = await axios.post(`http://127.0.0.1:8000/coin/api-v1/updateprice/${coinSymbol}`);
//       setCoinPriceList(prevState => ({
//         ...prevState,
//         [coinSymbol]: response.data.price,
//       }));
//     } catch (error) {
//       console.error(error);
//     }
//   }

//   async function handleSync() {
//     setLoading(true);
//     for (let i = 0; i < coinList.length; i += 3) {
//       const coinGroup = coinList.slice(i, i + 3);
//       const coinGroupPromises = coinGroup.map(coinSymbol => fetchCoinPrice(coinSymbol));
//       await Promise.all(coinGroupPromises);
//     }
//     setLoading(false);
//   }

//   return (
//     <div className="col-lg-1 col-xl-4">
//       <div className="card shadow mb-5" style={{ height: '415px', width: '500px' }}>
//         <div className="card-header py-3 d-flex flex-row align-items-center justify-content-between">
//           <h6 className="m-0 font-weight-bold text-primary">COIN LIST</h6>
//           <button className="btn btn-primary" onClick={handleSync} disabled={loading}>
//             {loading ? 'Syncing...' : 'Sync'}
//           </button>
//         </div>
//         <div className="card-body" style={{ overflowY: 'scroll', height: '300px' }}>
//           <div className="row">
//             {coinList.map(coinSymbol => (
//               <div className="col-md-4 mb-3" key={coinSymbol}>
//                 <div className="card h-100" style={{ padding: '10px' }}>
//                   <div className="card-body d-flex flex-column justify-content-between">
//                     <h5 className="card-title">{coinSymbol}</h5>
//                     <p className="card-text">{coinPriceList[coinSymbol] ? `$${coinPriceList[coinSymbol]}` : ''}</p>
//                     <button className="btn btn-secondary" onClick={() => fetchCoinPrice(coinSymbol)}>
//                       Get Price
//                     </button>
//                   </div>
//                 </div>
//               </div>
//             ))}
//           </div>
//         </div>
//       </div>
//     </div>
//   );
// }

// export default CoinList

import { useState, useEffect } from 'react';
import axios from 'axios';

function CoinList() {
  const [coinList, setCoinList] = useState([]);
  const [coinPriceList, setCoinPriceList] = useState({});
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    async function fetchCoinList() {
      try {
        const response = await axios.post('http://127.0.0.1:8000/coin/api-v1/coinsync', {"is_sync": "True"});
        setCoinList(response.data.coin_list);
      } catch (error) {
        console.error(error);
      }
    }
    fetchCoinList();
  }, []);

  async function fetchCoinPrice(coinSymbol) {
    try {
      const response = await axios.get(`http://127.0.0.1:8000/coin/api-v1/coinprice/${coinSymbol}`);
      setCoinPriceList(prevState => ({
        ...prevState,
        [coinSymbol]: response.data.price,
      }));
    } catch (error) {
      console.error(error);
    }
  }

  async function handleSync() {
    setLoading(true);
    for (let i = 0; i < coinList.length; i += 3) {
      const coinGroup = coinList.slice(i, i + 3);
      const coinGroupPromises = coinGroup.map(coinSymbol => fetchCoinPrice(coinSymbol));
      await Promise.all(coinGroupPromises);
    }
    setLoading(false);
  }

  return (
    <div className="col-lg-1 col-xl-4">
      <div className="card shadow mb-5" style={{ height: '415px', width: '500px' }}>
        <div className="card-header py-3 d-flex flex-row align-items-center justify-content-between">
          <h6 className="m-0 font-weight-bold text-primary">COIN LIST</h6>
          <button className="btn btn-primary" onClick={handleSync} disabled={loading}>
            {loading ? 'Syncing...' : 'Sync'}
          </button>
        </div>
        <div className="card-body" style={{ overflowY: 'scroll', height: '300px' }}>
          <div className="row">
            {coinList.map(coinSymbol => (
              <div className="col-md-4 mb-3" key={coinSymbol}>
                <div className="card h-100" style={{ padding: '10px' }}>
                  <div className="card-body d-flex flex-column justify-content-between">
                    <h5 className="card-title">{coinSymbol}</h5>
                    <p className="card-text">{coinPriceList[coinSymbol] ? `$${coinPriceList[coinSymbol]}` : ''}</p>
                    <button className="btn btn-secondary" onClick={() => fetchCoinPrice(coinSymbol)}>
                      Get Price
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default CoinList;
