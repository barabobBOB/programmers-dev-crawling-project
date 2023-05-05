import React, { useState, useEffect } from 'react';
import axios from 'axios';

const newsSymbolList = () => {
  const [currentSymbolPage, setCurrentSymbolPage] = useState(1);
  const [totalSymbolPages, setTotalSymbolPages] = useState(1);
  const [newsSymbolList, setNewsSymbolList] = useState([]);

  const getCoinSymbolNewsList = async (coinSymbol) => {
    try {
      const response = await axios.get(
        `http://127.0.0.1:8000/coin/api-v1/coinnews/${coinSymbol}?page=${currentSymbolPage}`,
      );
      console.log(response.data);
      setNewsSymbolList(response.data.results);
      setTotalSymbolPages(response.data.total_pages);
    } catch (error) {
      console.error(error);
    }
  };
  return { getCoinSymbolNewsList };
};

export default newsSymbolList;