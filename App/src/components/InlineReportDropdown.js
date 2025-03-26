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

  useEffect(() => {
    if (!company) return;

    fetch(`http://localhost:5000/api/sec_reports/${company}`)
      .then((res) => res.json())
      .then((data) => {
        if (data.reports) {
          setReports(data.reports);
        } else {
          setReports({});
        }
        setSelectedQuarter('');
        setUrl('');
      });
  }, [company]);

  const handleQuarterChange = (quarter) => {
    setSelectedQuarter(quarter);
    setUrl(reports[quarter] || '');
  };

  return (
    <div>
      <select
        className="form-select form-select-sm"
        onChange={(e) => handleQuarterChange(e.target.value)}
        value={selectedQuarter}
        style={{ minWidth: "160px" }}
      >
        <option value="">Select Quarter</option>
        {ALL_QUARTERS.map((qtr) => (
          <option key={qtr} value={qtr}>
            {qtr} {reports[qtr] ? "" : " (N/A)"}
          </option>
        ))}
      </select>

      {/* Show "View Report" button if URL exists */}
      {selectedQuarter && url && (
        <a
          href={url}
          target="_blank"
          rel="noopener noreferrer"
          style={{
            display: "inline-block",
            marginTop: "10px",
            backgroundColor: "#1a73e8",
            color: "white",
            padding: "8px 16px",
            borderRadius: "5px",
            textDecoration: "none",
            fontWeight: "500"
          }}
        >
          🔗 View {selectedQuarter} Report
        </a>
      )}

      {/* Show fallback message if no report */}
      {selectedQuarter && !url && (
        <p style={{ color: "#999", fontSize: "14px", marginTop: "8px" }}>
          No financial report found for {selectedQuarter}.
        </p>
      )}
    </div>
  );
};

export default InlineReportDropdown;
