import React, { useState, useEffect } from 'react';
import axios from 'axios';

const UseGetSymbolNews = ({ coinSymbol }) => {
  const [symbolNewsList, setSymbolNewsListData] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [symbolTotalPage, setSymbolTotalPage] = useState(1);

  useEffect(() => {
    const fetchNewsSymbolList = async (coinSymbol) => {
      try {
        const response = await axios.get(
          `http://127.0.0.1:8000/coin/api-v1/coinnews/${coinSymbol}?page=${currentPage}`,
        );
        setSymbolNewsListData(response.data.results);
        setSymbolTotalPage(response.data.total_pages);
        console.log(response.data);
      } catch (e) {
        console.error(e);
      }
    };
    fetchNewsSymbolList(coinSymbol);
  }, [currentPage, setSymbolNewsListData, setSymbolTotalPage, coinSymbol]);

  const handlePageChange = (page) => {
    setCurrentPage(page);
  };

  const renderPagination = () => {
    const pages = [];
    for (let i = 1; i <= symbolTotalPage; i++) {
      pages.push(
        <li
          key={i}
          className={`page-item${currentPage === i ? ' active' : ''}`}
        >
          <button className="page-link" onClick={() => handlePageChange(i)}>
            {i}
          </button>
        </li>,
      );
    }
    return (
      <nav>
        <ul className="pagination">
          <li className={`page-item${currentPage === 1 ? ' disabled' : ''}`}>
            <button
              className="page-link"
              onClick={() => handlePageChange(currentPage - 1)}
            >
              이전
            </button>
          </li>
          {pages}
          <li
            className={`page-item${
              currentPage === symbolTotalPage ? ' disabled' : ''
            }`}
          >
            <button
              className="page-link"
              onClick={() => handlePageChange(currentPage + 1)}
            >
              다음
            </button>
          </li>
        </ul>
      </nav>
    );
  };
  return (
    <>
      <div className="container-fluid">
        <div className="card shadow mb-4">
          <div className="card-header py-3">
            <h6 className="m-0 font-weight-bold text-primary">
              coin Symbol news
            </h6>
          </div>
          <div className="card-body">
            <div className="table-responsive">
              <table
                className="table table-bordered"
                id="dataTable"
                width="100%"
                cellSpacing="0"
              >
                <thead>
                  <tr>
                    <th>name</th>
                    <th>titles</th>
                    <th>urls</th>
                    <th>dates</th>
                  </tr>
                </thead>
                <tbody>
                  {symbolNewsList.map((news) => (
                    <tr key={news.id}>
                      <td style={{ fontSize: '10px' }}>{news.name}</td>
                      <td style={{ fontSize: '10px' }}>{news.titles}</td>
                      <td style={{ fontSize: '10px' }}>
                        <a href={news.urls}> {news.urls}</a>
                      </td>
                      <td style={{ fontSize: '13px' }}>{news.dates}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
              {renderPagination()}
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default UseGetSymbolNews;
