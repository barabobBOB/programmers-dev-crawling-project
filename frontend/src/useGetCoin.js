import React, { useState, useEffect } from 'react';
import axios from 'axios';

export const getOneCoinData = async (coinSymbol) => {
  try {
    const response = await axios.get(
      `http://127.0.0.1:8000/coin/api-v1/coinprice/${coinSymbol}`,
    );
    return response.data;

  } catch (e) {
    console.error(e);
  }
};
