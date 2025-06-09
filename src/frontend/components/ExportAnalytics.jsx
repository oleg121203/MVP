import React from 'react';
import axios from 'axios';

const ExportAnalytics = ({ projectId, metrics }) => {
  const handleExport = async (format) => {
    try {
      const response = await axios.get(
        `/api/v1/analytics/export/${projectId}/${format.toLowerCase()}`,
        { responseType: 'blob' }
      );
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `project_${projectId}_report.${format.toLowerCase()}`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      console.error('Export failed:', error);
      alert('Export failed. Please try again.');
    }
  };

  return (
    <div className="export-analytics">
      <h3>Export Analytics</h3>
      <div className="export-options">
        <button onClick={() => handleExport('PDF')}>PDF</button>
        <button onClick={() => handleExport('CSV')}>CSV</button>
        <button onClick={() => handleExport('Excel')}>Excel</button>
      </div>
    </div>
  );
};

export default ExportAnalytics;
