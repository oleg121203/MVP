import React from 'react';
import './Table.css';

/**
 * Reusable Table component for displaying tabular data
 *
 * @param {Object} props - Component props
 * @param {Array<{header: string, accessor: string, cell?: (row: object, rowIndex: number) => React.ReactNode}>} props.columns - Column definitions
 * @param {Array<object>} props.data - Data to display in the table
 * @param {boolean} [props.isLoading=false] - Whether the table is in loading state
 * @param {string} [props.emptyMessage="Немає даних"] - Message to display when there's no data
 * @param {string} [props.className] - Additional CSS classes for the table wrapper
 * @returns {JSX.Element} Table component
 */
const Table = ({
  columns,
  data,
  isLoading = false,
  emptyMessage = 'Немає даних',
  className = '',
}) => {
  // Render loading state
  if (isLoading) {
    return (
      <div className="table-container">
        <div className="table-loading">
          <div className="table-loading-spinner"></div>
          <p>Завантаження даних...</p>
        </div>
      </div>
    );
  }

  // Render empty state
  if (!data || data.length === 0) {
    return (
      <div className="table-container">
        <div className="table-empty">{emptyMessage}</div>
      </div>
    );
  }

  return (
    <div className={`table-container ${className}`}>
      <div className="table-responsive">
        <table className="custom-table">
          <thead>
            <tr>
              {columns.map((col) => (
                <th key={col.accessor || col.header}>{col.header}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {data.map((row, rowIndex) => (
              <tr key={row.id || `row-${rowIndex}`}>
                {columns.map((col) => (
                  <td key={`${rowIndex}-${col.accessor || col.header}`}>
                    {col.cell ? col.cell(row, rowIndex) : row[col.accessor]}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Table;
