import React, { useEffect, useState } from "react";

// Fixed list of all quarters
const ALL_QUARTERS = [
  "Q3 2022", "Q4 2022/Annual",
  "Q1 2023", "Q2 2023", "Q3 2023", "Q4 2023/Annual",
  "Q1 2024", "Q2 2024", "Q3 2024"
];

const InlineReportDropdown = ({ company }) => {
  const [reports, setReports] = useState({});
  const [selectedQuarter, setSelectedQuarter] = useState('');
  const [url, setUrl] = useState('');

  // Fetch SEC reports when company changes
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
      {/* Label + Dropdown */}
      <div style={{ display: "flex", alignItems: "center", gap: "5px", flexWrap: "nowrap" }}>
        <span style={{ fontWeight: "700", fontSize: "13px", whiteSpace: "nowrap" }}>
          Financial Report
        </span>

        <select
          className="form-select form-select-sm"
          onChange={(e) => handleQuarterChange(e.target.value)}
          value={selectedQuarter}
          style={{ minWidth: "180px" }}
        >
          <option value="">Select Quarter</option>
          {ALL_QUARTERS.map((qtr) => (
            <option key={qtr} value={qtr}>
              {qtr} {reports[qtr] ? "" : " (N/A)"}
            </option>
          ))}
        </select>
      </div>

      {/* View Report Button */}
      {selectedQuarter && url && (
        <a
          href={url}
          target="_blank"
          rel="noopener noreferrer"
          style={{
            display: "flex",
            marginTop: "5px",
            backgroundColor: "#1a73e8",
            color: "white",
            padding: "2px 8px",
            borderRadius: "3px",
            textDecoration: "none",
            fontWeight: "500"
          }}
        >
          🔗 View {selectedQuarter} Report
        </a>
      )}

      {/* No report available message */}
      {selectedQuarter && !url && (
        <p style={{ color: "#999", fontSize: "14px", marginTop: "8px" }}>
          No financial report found for {selectedQuarter}.
        </p>
      )}
    </div>
  );
};

export default InlineReportDropdown;
