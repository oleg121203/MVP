import React, { useState } from 'react';
import Button from './Button';
import Input from './Input';
import './SearchBar.css';

/**
 * SearchBar component for unified search experience across the application
 *
 * @param {Object} props
 * @param {string} props.placeholder - Placeholder text for the search input
 * @param {string} props.value - Initial value for the search input
 * @param {function} props.onSearch - Callback function when search is submitted (receives search query as parameter)
 * @param {boolean} props.isLoading - Whether the search is currently loading
 * @param {boolean} props.showClearButton - Whether to show a clear button
 * @param {string} props.buttonText - Text to display on the search button
 * @param {string} props.className - Additional CSS class for the search bar
 * @param {boolean} props.autoFocus - Whether to autofocus the search input
 */
const SearchBar = ({
  placeholder = 'Search...',
  value = '',
  onSearch,
  isLoading = false,
  showClearButton = true,
  buttonText = 'Search',
  className = '',
  autoFocus = false,
}) => {
  const [searchQuery, setSearchQuery] = useState(value);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (onSearch && searchQuery.trim()) {
      onSearch(searchQuery.trim());
    }
  };

  const handleClear = () => {
    setSearchQuery('');
    // If onSearch is provided, call it with empty string to reset search
    if (onSearch) {
      onSearch('');
    }
  };

  return (
    <form className={`search-bar ${className}`} onSubmit={handleSubmit}>
      <div className="search-input-container">
        <Input
          type="text"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder={placeholder}
          className="search-input"
          autoFocus={autoFocus}
          disabled={isLoading}
        />
        {showClearButton && searchQuery && (
          <button
            type="button"
            className="clear-button"
            onClick={handleClear}
            aria-label="Clear search"
          >
            ×
          </button>
        )}
      </div>
      <Button
        type="submit"
        variant="primary"
        isLoading={isLoading}
        disabled={!searchQuery.trim() || isLoading}
        className="search-button"
      >
        {isLoading ? 'Searching...' : buttonText}
      </Button>
    </form>
  );
};

export default SearchBar;
