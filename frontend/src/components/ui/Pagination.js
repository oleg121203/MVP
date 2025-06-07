import React from 'react';
import Button from './Button';
import './Pagination.css';

/**
 * Pagination component for navigating through pages of data
 *
 * @param {Object} props - Component props
 * @param {number} props.currentPage - Current active page (1-indexed)
 * @param {number} props.totalPages - Total number of pages
 * @param {Function} props.onPageChange - Function called when page changes
 * @param {number} [props.itemsPerPage] - Number of items per page
 * @param {number} [props.totalItems] - Total number of items
 * @param {number} [props.maxVisibleButtons=5] - Maximum number of page buttons to show
 * @param {boolean} [props.showFirstLast=false] - Whether to show first/last page buttons
 * @param {string} [props.className] - Additional CSS class
 * @returns {JSX.Element|null} Pagination component or null if only one page
 */
const Pagination = ({
  currentPage,
  totalPages,
  onPageChange,
  itemsPerPage,
  totalItems,
  maxVisibleButtons = 5,
  showFirstLast = false,
  className = '',
}) => {
  // Don't render pagination if there's only one page
  if (totalPages <= 1) {
    return null;
  }

  const handlePageClick = (pageNumber) => {
    if (pageNumber >= 1 && pageNumber <= totalPages && pageNumber !== currentPage) {
      onPageChange(pageNumber);
    }
  };

  // Calculate which page numbers to display
  const getPageNumbers = () => {
    const pageNumbers = [];

    // If total pages is less than or equal to max visible buttons, show all pages
    if (totalPages <= maxVisibleButtons) {
      for (let i = 1; i <= totalPages; i++) {
        pageNumbers.push({ type: 'page', value: i });
      }
      return pageNumbers;
    }

    // Always show first page
    pageNumbers.push({ type: 'page', value: 1 });

    // Calculate start and end of visible page range
    let startPage = Math.max(2, currentPage - Math.floor(maxVisibleButtons / 2));
    let endPage = Math.min(totalPages - 1, startPage + maxVisibleButtons - 3);

    // Adjust if we're near the beginning
    if (startPage === 2) {
      endPage = Math.min(totalPages - 1, maxVisibleButtons - 1);
    }

    // Adjust if we're near the end
    if (endPage === totalPages - 1) {
      startPage = Math.max(2, totalPages - maxVisibleButtons + 2);
    }

    // Add ellipsis after first page if needed
    if (startPage > 2) {
      pageNumbers.push({ type: 'ellipsis', value: 'start' });
    }

    // Add visible page numbers
    for (let i = startPage; i <= endPage; i++) {
      pageNumbers.push({ type: 'page', value: i });
    }

    // Add ellipsis before last page if needed
    if (endPage < totalPages - 1) {
      pageNumbers.push({ type: 'ellipsis', value: 'end' });
    }

    // Always show last page
    if (totalPages > 1) {
      pageNumbers.push({ type: 'page', value: totalPages });
    }

    return pageNumbers;
  };

  const pageNumbers = getPageNumbers();

  // Display info about items shown (e.g., "Showing 1-10 of 100")
  const renderItemsInfo = () => {
    if (!itemsPerPage || !totalItems) return null;

    const start = (currentPage - 1) * itemsPerPage + 1;
    const end = Math.min(currentPage * itemsPerPage, totalItems);

    return (
      <div className="pagination-info">
        Showing {start}-{end} of {totalItems}
      </div>
    );
  };

  return (
    <nav className={`pagination-container ${className}`} aria-label="Page navigation">
      {renderItemsInfo()}

      <ul className="pagination-list">
        {/* First page button */}
        {showFirstLast && (
          <li className="pagination-item">
            <Button
              variant="icon"
              onClick={() => handlePageClick(1)}
              disabled={currentPage === 1}
              className="pagination-button first"
              aria-label="First page"
            >
              &laquo;
            </Button>
          </li>
        )}

        {/* Previous page button */}
        <li className="pagination-item">
          <Button
            variant="icon"
            onClick={() => handlePageClick(currentPage - 1)}
            disabled={currentPage === 1}
            className="pagination-button prev"
            aria-label="Previous page"
          >
            &lsaquo;
          </Button>
        </li>

        {/* Page number buttons */}
        {pageNumbers.map((item, index) => (
          <li
            key={`${item.type}-${item.value}-${index}`}
            className={`pagination-item ${item.type === 'page' && currentPage === item.value ? 'active' : ''}`}
          >
            {item.type === 'page' ? (
              <Button
                variant={currentPage === item.value ? 'primary' : 'secondary'}
                onClick={() => handlePageClick(item.value)}
                className="pagination-button page"
                aria-current={currentPage === item.value ? 'page' : undefined}
                aria-label={`Page ${item.value}`}
              >
                {item.value}
              </Button>
            ) : (
              <span className="pagination-ellipsis">&hellip;</span>
            )}
          </li>
        ))}

        {/* Next page button */}
        <li className="pagination-item">
          <Button
            variant="icon"
            onClick={() => handlePageClick(currentPage + 1)}
            disabled={currentPage === totalPages}
            className="pagination-button next"
            aria-label="Next page"
          >
            &rsaquo;
          </Button>
        </li>

        {/* Last page button */}
        {showFirstLast && (
          <li className="pagination-item">
            <Button
              variant="icon"
              onClick={() => handlePageClick(totalPages)}
              disabled={currentPage === totalPages}
              className="pagination-button last"
              aria-label="Last page"
            >
              &raquo;
            </Button>
          </li>
        )}
      </ul>
    </nav>
  );
};

export default Pagination;
