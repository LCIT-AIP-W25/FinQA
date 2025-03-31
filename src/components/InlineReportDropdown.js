import React, { useEffect, useState } from "react";

const ALL_QUARTERS = [
  "Q3 2022", "Q4 2022/Annual",
  "Q1 2023", "Q2 2023", "Q3 2023", "Q4 2023/Annual",
  "Q1 2024", "Q2 2024", "Q3 2024"
];

const InlineReportDropdown = ({ company }) => {
  const [reports, setReports] = useState({});
  const [selectedQuarter, setSelectedQuarter] = useState('');
  const [url, setUrl] = useState('');
  const CHATBOT_API_URL = "https://finqa-app-w15r.onrender.com";

  useEffect(() => {
    if (!company) return;

    fetch(`${CHATBOT_API_URL}/api/sec_reports/${company}`)
      .then((res) => res.json())
      .then((data) => {
        setReports(data.reports || {});
        setSelectedQuarter('');
        setUrl('');
      });
  }, [company]);

  const handleQuarterChange = (quarter) => {
    setSelectedQuarter(quarter);
    setUrl(reports[quarter] || '');
  };

  const getShortQuarter = (quarter) => {
    if (!quarter) return '';
    return quarter.includes('/Annual') 
      ? quarter.split('/')[0].replace('Q', 'Q') 
      : quarter.replace(' ', '\'');
  };

  return (
    <div className="report-dropdown-container">
      <select
        className="quarter-select"
        onChange={(e) => handleQuarterChange(e.target.value)}
        value={selectedQuarter}
      >
        <option value="">Select Financial Quarter</option>
        {ALL_QUARTERS.map((qtr) => (
          <option key={qtr} value={qtr}>
            {qtr} {reports[qtr] ? "" : " (N/A)"}
          </option>
        ))}
      </select>

      {selectedQuarter && url && (
        <a
          href={url}
          target="_blank"
          rel="noopener noreferrer"
          className="report-link"
        >
          🔗 View {getShortQuarter(selectedQuarter)} Report
        </a>
      )}

      {selectedQuarter && !url && (
        <p className="no-report-message">
          No report available for {getShortQuarter(selectedQuarter)}
        </p>
      )}

      <style jsx>{`
        .report-dropdown-container {
          width: 100%;
          margin-bottom: 10px;
        }
        
        .quarter-select {
          width: 100%;
          padding: 8px 12px;
          border-radius: 4px;
          border: 1px solid #ddd;
          font-size: 14px;
          background-color: white;
          cursor: pointer;
        }
        
        .report-link {
          display: block;
          margin-top: 8px;
          background-color: #1a73e8;
          color: white;
          padding: 6px 12px;
          border-radius: 4px;
          text-decoration: none;
          font-weight: 500;
          font-size: 13px;
          text-align: center;
        }
        
        .no-report-message {
          color: #999;
          font-size: 12px;
          margin-top: 8px;
          text-align: center;
        }
        
        @media (max-width: 768px) {
          .quarter-select {
            font-size: 13px;
            padding: 6px 10px;
          }
          
          .report-link {
            font-size: 12px;
            padding: 5px 10px;
          }
        }
      `}</style>
    </div>
  );
};

export default InlineReportDropdown;