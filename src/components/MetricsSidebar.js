// MetricsSidebar.js
import React from "react";
import "../styles/MetricsSidebar.css";

function MetricsSidebar({
  selectedCompany,
  metricsSearchTerm,
  setMetricsSearchTerm,
  filteredMetrics,
  selectedMetric,
  handleMetricClick,
  setShowMetricsSidebar
}) {
  return (
    <div className="metrics-sidebar">
      <div className="metrics-header-container">
        <h3 className="metrics-header">Available Financial Metrics</h3>
        
        <div className="metrics-controls">
          
          <div className="metrics-search">
            <input
              type="text"
              placeholder="Search metrics..."
              value={metricsSearchTerm}
              onChange={(e) => setMetricsSearchTerm(e.target.value)}
              className="metrics-search-input"
            />
          </div>
        </div>
        
        <div className="metrics-header-com">Select a company to view available metrics and ask the chatbot for details.</div>
      </div>
      
      <div className="metrics-scroll-container">
        {filteredMetrics.length > 0 ? (
          <div className="metrics-container">
            {filteredMetrics.map((metric, index) => (
              <div 
                key={index} 
                className={`metric-item ${
                  selectedMetric === metric ? 'selected' : 
                  metricsSearchTerm && 
                  metric.toLowerCase().includes(metricsSearchTerm.toLowerCase()) 
                  ? 'highlight' 
                  : ''
                }`}
                onClick={() => {
                  handleMetricClick(metric);
                  if (window.innerWidth < 768) {
                    setShowMetricsSidebar(false);  // Auto-close on mobile
                  }
                }}
                
              >
                {metric}
              </div>
            ))}
          </div>
        ) : (
          <p className="no-metrics">
            {metricsSearchTerm ? "No matching metrics found" : "No metrics available"}
          </p>
        )}
      </div>
    </div>
  );
}

export default MetricsSidebar;