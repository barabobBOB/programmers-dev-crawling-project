import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Newslist = () => {
  const [newsList, setNewsList] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  useEffect(() => {
    const fetchNewsList = async () => {
      try {
        const response = await axios.get(
          `http://127.0.0.1:8000/coin/api-v1/recentnews?page=${currentPage}`,
        );
        setNewsList(response.data.results);
        setTotalPages(response.data.total_pages);
      } catch (error) {
        console.error(error);
      }
    };
    fetchNewsList();
  }, [currentPage]);

  const handlePageChange = (page) => {
    setCurrentPage(page);
  };

  const handleSyncClick = async () => {
    try {
      const response = await axios.get(
        'http://127.0.0.1:8000/coin/api-v1/recentnews/crawling',
      );
      setCurrentPage(1);
      setNewsList(response.data.results);
      setTotalPages(response.data.total_pages);
    } catch (error) {
      console.error(error);
    }
  };
  const renderPagination = () => {
    const pages = [];
    for (let i = 1; i <= totalPages; i++) {
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
              currentPage === totalPages ? ' disabled' : ''
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
            <h6 className="m-0 font-weight-bold text-primary">coin news</h6>
          </div>
          <button className="btn btn-primary" onClick={handleSyncClick}>
            Sync
          </button>
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
                    <th>date</th>
                    <th>time</th>
                    <th>title</th>
                    <th>content</th>
                  </tr>
                </thead>
                <tbody>
                  {newsList.map((news) => (
                    <tr key={news.id}>
                      <td style={{ fontSize: '10px' }}>{news.date}</td>
                      <td style={{ fontSize: '10px' }}>{news.time}</td>
                      <td style={{ fontSize: '10px' }}>{news.title}</td>
                      <td style={{ fontSize: '13px' }}>{news.content}</td>
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

export default Newslist;
