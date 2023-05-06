import axios from 'axios';

export const getCoinSymbolNewsList = async (coinSymbol) => {
try {
    const response = await axios.get(
    `http://127.0.0.1:8000/coin/api-v1/coinnews/${coinSymbol}`,
    );
    console.log(response.data);
    setNewsSymbolList(response.data.results);
    setTotalSymbolPages(response.data.total_pages);
} catch (error) {
    console.error(error);
}
};