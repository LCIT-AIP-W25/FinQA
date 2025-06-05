import React from "react";
import InlineReportDropdown from "./InlineReportDropdown";
import "../styles/CompanyReportPanel.css";

function CompanyReportPanel({
  searchTerm,
  setSearchTerm,
  companyList,
  selectedCompany,
  setSelectedCompany,
  handleFileUpload,
  uploadStatus,
  uploadMessage,
  hoverMessage,
  setUploadMessage,
  setShowCompanyPanel 
}) {
  return (
    <div className="company-report-panel">
      {/* Company Selection */}
      <div className="company-section">
        <h5 className="panel-title">Select Company</h5>
        <input
          type="text"
          placeholder="Search company..."
          className="company-search-input"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
        <div className="company-list">
          {companyList
            .filter((company) =>
              company.toLowerCase().includes(searchTerm.toLowerCase())
            )
            .map((company) => (
              <div
                key={company}
                className={`company-item ${
                  selectedCompany === company ? "selected" : ""
                }`}
                onClick={() => {
                  setSelectedCompany(company);
                  if (window.innerWidth < 768) {
                    setShowCompanyPanel(false);  // Auto-close on mobile
                  }
                }}
              >
                {company}
              </div>
            ))}
        </div>
      </div>

      {/* Inline Report Dropdown */}
      <div className="report-section">
        <h5 className="panel-title">Browse Official Financial Reports</h5>
        <p className="panel-subtext">
          Please select a company to browse reports.
        </p>
        <div className="inline-report-dropdown">
          <InlineReportDropdown company={selectedCompany} />
        </div>
      </div>

      {/* PDF Upload Section */}
      <div className="upload-section">
        <h5 className="panel-title">Open PDF Mode</h5>
          <p className="panel-subtext">
            Upload a PDF to ask questions from it using WealthWiz AI.
          </p>

        <input
          type="file"
          id="pdfUpload"
          accept="application/pdf"
          style={{ display: "none" }}
          onChange={handleFileUpload}
        />
        <button
          className="chat-app-upload-btn"
          onClick={() => document.getElementById("pdfUpload").click()}
        >
          📄 Upload PDF
        </button>

        {/* Upload Status Icon with Hover Effect */}
        {uploadStatus && (
          <span
            className="upload-status-icon"
            data-hover={hoverMessage}
            onMouseEnter={() => setUploadMessage(hoverMessage)}
            onMouseLeave={() =>
              setUploadMessage(uploadStatus === "error" ? "❌" : "⏳")
            }
          >
            {uploadMessage}
          </span>
        )}
      </div>
    </div>
  );
}

export default CompanyReportPanel;
