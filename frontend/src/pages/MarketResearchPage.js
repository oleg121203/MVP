import React, { useState, useEffect, useCallback, useMemo } from 'react';
import { useAuth } from '../context/AuthContext';
import { useToast } from '../context/ToastContext';
import { useTheme } from '../context/ThemeContext';
import { useLocalization } from '../context/LocalizationContext';
import {
  researchMarketPrices,
  getMarketResearchHistory,
  getMarketResearchQueryDetails,
  getMarketPricesForQuery,
} from '../services/apiService';
import { Button, Input, Table, Pagination, SearchBar, Card } from '../components/ui';

const MarketResearchPage = () => {
  const { token } = useAuth();
  const toast = useToast();
  const { theme } = useTheme();
  const { t } = useLocalization();
  const [componentName, setComponentName] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [report, setReport] = useState('');
  const [prices, setPrices] = useState([]);
  const [queryId, setQueryId] = useState(null);
  const [researchHistory, setResearchHistory] = useState([]);
  const [isHistoryLoading, setIsHistoryLoading] = useState(false);

  // Pagination state for history
  const [historyPage, setHistoryPage] = useState(1);
  const [totalHistoryItems, setTotalHistoryItems] = useState(0);
  const [historyItemsPerPage] = useState(6);

  // Pagination state for prices
  const [pricesPage, setPricesPage] = useState(1);
  const [totalPrices, setTotalPrices] = useState(0);
  const [pricesPerPage] = useState(10);
  const [isPricesLoading, setIsPricesLoading] = useState(false);

  // Filtering and sorting state
  const [priceFilter, setPriceFilter] = useState('');
  const [sortField, setSortField] = useState('min_price');
  const [sortDirection, setSortDirection] = useState('asc');

  // Interactive report sections
  const [expandedSections, setExpandedSections] = useState({
    overview: true,
    recommendations: true,
    priceAnalysis: true,
    fullReport: false,
  });

  // Parse report sections if available
  const [parsedReport, setParsedReport] = useState({
    overview: '',
    recommendations: [],
    priceAnalysis: '',
  });

  // Parse report text into sections for better interactivity
  const parseReportIntoSections = (reportText) => {
    if (!reportText)
      return {
        overview: '',
        recommendations: [],
        priceAnalysis: '',
      };

    // Try to identify different sections in the report
    const sections = {
      overview: '',
      recommendations: [],
      priceAnalysis: '',
    };

    // Extract overview (first paragraph or two)
    const paragraphs = reportText.split('\n\n');
    sections.overview = paragraphs[0];

    // Look for recommendations (often preceded by keywords)
    const recommendationKeywords = ['recommend', 'suggestion', 'advice', 'consider'];
    const recommendationLines = reportText.split('\n').filter((line) => {
      const lowerLine = line.toLowerCase();
      return (
        recommendationKeywords.some((keyword) => lowerLine.includes(keyword)) ||
        lowerLine.includes('should') ||
        lowerLine.startsWith('- ') ||
        lowerLine.startsWith('• ')
      );
    });

    sections.recommendations = recommendationLines.map((line) => {
      // Clean up bullet points
      return line.replace(/^[-•*]\s+/, '');
    });

    // Extract price analysis (paragraphs mentioning price, cost, range, etc.)
    const priceKeywords = [
      'price',
      'cost',
      'range',
      'expensive',
      'affordable',
      'cheap',
      'uah',
      'hryvnia',
    ];
    const priceAnalysisParagraphs = paragraphs.filter((para) => {
      const lowerPara = para.toLowerCase();
      return priceKeywords.some((keyword) => lowerPara.includes(keyword));
    });

    if (priceAnalysisParagraphs.length > 0) {
      sections.priceAnalysis = priceAnalysisParagraphs.join('\n\n');
    } else {
      // If no specific price analysis found, use the second paragraph as a fallback
      sections.priceAnalysis = paragraphs.length > 1 ? paragraphs[1] : '';
    }

    return sections;
  };

  const handleResearch = async (searchQuery) => {
    // If called from the SearchBar component, use the passed query
    // Otherwise, use the state value (for backward compatibility)
    const query = searchQuery || componentName;

    if (!query.trim()) {
      toast.error(t('Please enter a component name.'));
      return;
    }

    // Update componentName state if it was passed from SearchBar
    if (searchQuery) {
      setComponentName(searchQuery);
    }

    setIsLoading(true);
    setReport('');
    setParsedReport({ overview: '', recommendations: [], priceAnalysis: '' });
    setPrices([]);
    setQueryId(null);
    setPricesPage(1);
    setTotalPrices(0);
    // Reset filters and sorting
    setPriceFilter('');
    setSortField('min_price');
    setSortDirection('asc');

    try {
      // Using our API service
      const data = await researchMarketPrices(query);

      setReport(data.text_report);

      // Parse the report into sections
      const parsedSections = parseReportIntoSections(data.text_report);
      setParsedReport(parsedSections);

      setQueryId(data.id);

      // Fetch the first page of prices
      if (data.id) {
        fetchPricesForQuery(data.id, 1);
        toast.success(t('Market research for "{{query}}" completed successfully', { query }));
      }

      // Refresh the research history
      fetchResearchHistory();
    } catch (err) {
      toast.error(t('Research failed: {{message}}', { message: err.message }));
    } finally {
      setIsLoading(false);
    }
  };

  const fetchResearchHistory = useCallback(
    async (page = 1) => {
      setIsHistoryLoading(true);
      try {
        const skip = (page - 1) * historyItemsPerPage;
        // Using our API service
        const data = await getMarketResearchHistory(skip, historyItemsPerPage);
        setResearchHistory(data.queries || []);
        setTotalHistoryItems(data.total || 0);
        setHistoryPage(page);
      } catch (err) {
        console.error('Error fetching research history:', err);
        toast.error(t('Failed to load research history: {{message}}', { message: err.message }));
      } finally {
        setIsHistoryLoading(false);
      }
    },
    [historyItemsPerPage, toast, t]
  );

  const handleHistoryPageChange = (page) => {
    fetchResearchHistory(page);
  };

  const fetchPricesForQuery = useCallback(
    async (id, page = 1) => {
      if (!id) return;

      setIsPricesLoading(true);
      try {
        const skip = (page - 1) * pricesPerPage;
        const data = await getMarketPricesForQuery(id, skip, pricesPerPage);
        setPrices(data.prices || []);
        setTotalPrices(data.total || 0);
        setPricesPage(page);
      } catch (err) {
        console.error('Error fetching prices:', err);
        toast.error(t('Failed to load price data: {{message}}', { message: err.message }));
      } finally {
        setIsPricesLoading(false);
      }
    },
    [pricesPerPage, toast, t]
  );

  const handlePricesPageChange = (page) => {
    if (queryId) {
      fetchPricesForQuery(queryId, page);
    }
  };

  const loadResearchQuery = async (id) => {
    if (!id) return;

    setIsLoading(true);
    setPrices([]);
    setPricesPage(1);
    setTotalPrices(0);
    setPriceFilter('');
    setSortField('min_price');
    setSortDirection('asc');

    try {
      // Get the query details
      const data = await getMarketResearchQueryDetails(id);

      setComponentName(data.query_text || '');
      setReport(data.text_report || '');

      // Parse the report into sections
      const parsedSections = parseReportIntoSections(data.text_report);
      setParsedReport(parsedSections);

      setQueryId(id);

      // Fetch the first page of prices
      fetchPricesForQuery(id, 1);
      toast.info(
        t('Loaded research for "{{componentName}}"', { componentName: data.query_text || '' })
      );
    } catch (err) {
      console.error('Error loading research query:', err);
      toast.error(t('Failed to load research data: {{message}}', { message: err.message }));
    } finally {
      setIsLoading(false);
    }
  };

  // Toggle section expansion
  const toggleSection = (section) => {
    setExpandedSections((prev) => ({
      ...prev,
      [section]: !prev[section],
    }));
  };

  // Filter and sort price data
  const getFilteredAndSortedPrices = useMemo(() => {
    if (!prices.length) return [];

    // First, filter the prices
    let filteredPrices = prices;
    if (priceFilter) {
      const filter = priceFilter.toLowerCase();
      filteredPrices = prices.filter((price) => {
        return (
          (price.component && price.component.toLowerCase().includes(filter)) ||
          (price.store_name && price.store_name.toLowerCase().includes(filter)) ||
          (price.unit && price.unit.toLowerCase().includes(filter))
        );
      });
    }

    // Then, sort the filtered prices
    return [...filteredPrices].sort((a, b) => {
      let aValue = a[sortField];
      let bValue = b[sortField];

      // Handle numeric fields
      if (sortField === 'min_price' || sortField === 'max_price' || sortField === 'store_price') {
        aValue = parseFloat(aValue) || 0;
        bValue = parseFloat(bValue) || 0;
      }
      // Handle string fields
      else if (typeof aValue === 'string' && typeof bValue === 'string') {
        aValue = aValue.toLowerCase();
        bValue = bValue.toLowerCase();
      }

      // Perform the comparison
      if (aValue < bValue) return sortDirection === 'asc' ? -1 : 1;
      if (aValue > bValue) return sortDirection === 'asc' ? 1 : -1;
      return 0;
    });
  }, [prices, priceFilter, sortField, sortDirection]);

  const handleSortChange = (field) => {
    // If clicking the same field, toggle direction
    if (field === sortField) {
      setSortDirection((prev) => (prev === 'asc' ? 'desc' : 'asc'));
    }
    // Otherwise, set the new field and default to ascending
    else {
      setSortField(field);
      setSortDirection('asc');
    }
  };

  // Load research history when component mounts
  useEffect(() => {
    if (token) {
      fetchResearchHistory();
    }
  }, [token, fetchResearchHistory]);

  return (
    <div className="max-w-7xl mx-auto p-4 md:p-6 lg:p-8">
      <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100 mb-4">
        {t('Market Price Monitoring')}
      </h1>
      <p className="text-lg text-gray-700 dark:text-gray-300 mb-8">
        {t('Enter a component name to get a price report from the AI assistant.')}
      </p>

      {/* Search Bar */}
      <div className="mb-10 w-full max-w-3xl mx-auto">
        <SearchBar
          placeholder={t('Enter component name (e.g., "AMD Ryzen 5600X", "RTX 3080")')}
          onSearch={handleResearch}
          isLoading={isLoading}
          buttonText={t('Research')}
          autoFocus
        />
      </div>

      {/* Research Results */}
      {report && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mt-8">
          {/* AI Report Section */}
          <div className="lg:col-span-1">
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 border border-gray-200 dark:border-gray-700">
              <h3 className="text-xl font-semibold text-gray-800 dark:text-gray-100 mb-6 pb-2 border-b border-gray-200 dark:border-gray-700">
                {t('Research Results for')} "{componentName}"
              </h3>

              {/* Overview Section */}
              <div className="mb-4">
                <button
                  onClick={() => toggleSection('overview')}
                  className="flex justify-between items-center w-full text-left font-medium text-gray-700 dark:text-gray-300 py-2 hover:text-blue-600 dark:hover:text-blue-400 transition-colors duration-150"
                >
                  <span className="text-lg">{t('Overview')}</span>
                  <span className="transform transition-transform duration-200">
                    {expandedSections.overview ? (
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        className="h-5 w-5"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M5 15l7-7 7 7"
                        />
                      </svg>
                    ) : (
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        className="h-5 w-5"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M19 9l-7 7-7-7"
                        />
                      </svg>
                    )}
                  </span>
                </button>

                {expandedSections.overview && (
                  <div className="mt-2 text-gray-600 dark:text-gray-400 leading-relaxed">
                    {parsedReport.overview}
                  </div>
                )}
              </div>

              {/* Price Analysis Section */}
              <div className="mb-4">
                <button
                  onClick={() => toggleSection('priceAnalysis')}
                  className="flex justify-between items-center w-full text-left font-medium text-gray-700 dark:text-gray-300 py-2 hover:text-blue-600 dark:hover:text-blue-400 transition-colors duration-150"
                >
                  <span className="text-lg">{t('Price Analysis')}</span>
                  <span className="transform transition-transform duration-200">
                    {expandedSections.priceAnalysis ? (
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        className="h-5 w-5"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M5 15l7-7 7 7"
                        />
                      </svg>
                    ) : (
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        className="h-5 w-5"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M19 9l-7 7-7-7"
                        />
                      </svg>
                    )}
                  </span>
                </button>

                {expandedSections.priceAnalysis && (
                  <div className="mt-2 text-gray-600 dark:text-gray-400 leading-relaxed">
                    {parsedReport.priceAnalysis}
                  </div>
                )}
              </div>

              {/* Recommendations Section */}
              <div className="mb-4">
                <button
                  onClick={() => toggleSection('recommendations')}
                  className="flex justify-between items-center w-full text-left font-medium text-gray-700 dark:text-gray-300 py-2 hover:text-blue-600 dark:hover:text-blue-400 transition-colors duration-150"
                >
                  <span className="text-lg">{t('Recommendations')}</span>
                  <span className="transform transition-transform duration-200">
                    {expandedSections.recommendations ? (
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        className="h-5 w-5"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M5 15l7-7 7 7"
                        />
                      </svg>
                    ) : (
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        className="h-5 w-5"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M19 9l-7 7-7-7"
                        />
                      </svg>
                    )}
                  </span>
                </button>

                {expandedSections.recommendations && (
                  <div className="mt-2">
                    <ul className="list-disc pl-5 space-y-2 text-gray-600 dark:text-gray-400">
                      {parsedReport.recommendations.length > 0 ? (
                        parsedReport.recommendations.map((rec, index) => (
                          <li key={index} className="leading-relaxed">
                            {rec}
                          </li>
                        ))
                      ) : (
                        <li>{t('No specific recommendations found.')}</li>
                      )}
                    </ul>
                  </div>
                )}
              </div>

              {/* Full Report Toggle */}
              <div className="mt-6 pt-4 border-t border-gray-200 dark:border-gray-700">
                <Button
                  onClick={() => toggleSection('fullReport')}
                  variant="text"
                  className="text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300 transition-colors duration-150"
                >
                  {expandedSections.fullReport ? t('Hide Full Report') : t('Show Full Report')}
                </Button>

                {expandedSections.fullReport && (
                  <div className="mt-4 p-4 bg-gray-50 dark:bg-gray-900 rounded-md border border-gray-200 dark:border-gray-700 text-gray-600 dark:text-gray-400 whitespace-pre-wrap">
                    {report}
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Price Data Table */}
          <div className="lg:col-span-1">
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 border border-gray-200 dark:border-gray-700">
              <h3 className="text-xl font-semibold text-gray-800 dark:text-gray-100 mb-6 pb-2 border-b border-gray-200 dark:border-gray-700">
                {t('Price Data')}
              </h3>

              <div className="flex flex-col sm:flex-row gap-3 mb-4">
                <div className="w-full sm:w-auto">
                  <Input
                    type="text"
                    placeholder={t('Filter prices...')}
                    value={priceFilter}
                    onChange={(e) => setPriceFilter(e.target.value)}
                    className="w-full"
                  />
                </div>

                <div className="flex space-x-2">
                  <Button
                    onClick={() => handleSortChange('min_price')}
                    variant={sortField === 'min_price' ? 'primary' : 'secondary'}
                    size="sm"
                    className="whitespace-nowrap"
                  >
                    {t('Sort by Price')}{' '}
                    {sortField === 'min_price' && (sortDirection === 'asc' ? '↑' : '↓')}
                  </Button>

                  <Button
                    onClick={() => handleSortChange('store_name')}
                    variant={sortField === 'store_name' ? 'primary' : 'secondary'}
                    size="sm"
                    className="whitespace-nowrap"
                  >
                    {t('Sort by Store')}{' '}
                    {sortField === 'store_name' && (sortDirection === 'asc' ? '↑' : '↓')}
                  </Button>
                </div>
              </div>

              <div className="overflow-x-auto">
                <Table
                  columns={[
                    {
                      header: t('Component'),
                      accessor: 'component',
                      sortable: true,
                      cell: (row) => (
                        <div className="font-medium text-gray-800 dark:text-gray-200">
                          {row.component || t('N/A')}
                        </div>
                      ),
                    },
                    {
                      header: t('Price Range'),
                      accessor: 'min_price',
                      sortable: true,
                      cell: (row) => (
                        <div>
                          {row.min_price && row.max_price ? (
                            <span>
                              {parseFloat(row.min_price).toLocaleString()} -{' '}
                              {parseFloat(row.max_price).toLocaleString()} {row.currency || 'UAH'}
                            </span>
                          ) : (
                            t('N/A')
                          )}
                        </div>
                      ),
                    },
                    {
                      header: t('Unit'),
                      accessor: 'unit',
                      cell: (row) => row.unit || t('N/A'),
                    },
                    {
                      header: t('Store'),
                      accessor: 'store_name',
                      sortable: true,
                      cell: (row) => row.store_name || t('N/A'),
                    },
                    {
                      header: t('Store Price'),
                      accessor: 'store_price',
                      sortable: true,
                      cell: (row) => {
                        if (!row.store_price) return t('N/A');

                        return (
                          <div className="flex items-center">
                            <span className="font-medium">
                              {parseFloat(row.store_price).toLocaleString()} {row.currency || 'UAH'}
                            </span>

                            {row.store_url && (
                              <a
                                href={row.store_url}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="ml-2 text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300"
                              >
                                <svg
                                  xmlns="http://www.w3.org/2000/svg"
                                  className="h-5 w-5"
                                  fill="none"
                                  viewBox="0 0 24 24"
                                  stroke="currentColor"
                                >
                                  <path
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                    strokeWidth={2}
                                    d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"
                                  />
                                </svg>
                              </a>
                            )}
                          </div>
                        );
                      },
                    },
                  ]}
                  data={getFilteredAndSortedPrices}
                  isLoading={isPricesLoading}
                  emptyMessage={
                    priceFilter ? t('No matching price data') : t('No price data available')
                  }
                />
              </div>

              {totalPrices > pricesPerPage && (
                <div className="mt-4">
                  <Pagination
                    currentPage={pricesPage}
                    totalPages={Math.ceil(totalPrices / pricesPerPage)}
                    onPageChange={handlePricesPageChange}
                    itemsPerPage={pricesPerPage}
                    totalItems={totalPrices}
                    maxVisibleButtons={5}
                    showFirstLast={true}
                  />
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Recent Searches History */}
      <div className="mt-8">
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 border border-gray-200 dark:border-gray-700">
          <h3 className="text-xl font-semibold text-gray-800 dark:text-gray-100 mb-6 pb-2 border-b border-gray-200 dark:border-gray-700">
            {t('Recent Searches')}
          </h3>

          {isHistoryLoading ? (
            <div className="flex flex-col items-center justify-center py-8">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 dark:border-blue-400"></div>
              <p className="mt-4 text-gray-600 dark:text-gray-400">
                {t('Loading search history...')}
              </p>
            </div>
          ) : researchHistory.length > 0 ? (
            <>
              <div className="space-y-2">
                {researchHistory.map((item) => (
                  <div
                    key={item.id}
                    className="group cursor-pointer p-3 hover:bg-gray-50 dark:hover:bg-gray-750 rounded-md border-l-4 border-transparent hover:border-blue-500 dark:hover:border-blue-400 transition-all duration-150"
                    onClick={() => loadResearchQuery(item.id)}
                  >
                    <div className="flex justify-between items-center">
                      <div className="flex-1">
                        <div className="font-medium text-gray-800 dark:text-gray-200 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors duration-150">
                          {item.query_text}
                        </div>
                        <div className="text-sm text-gray-500 dark:text-gray-400">
                          {new Date(item.created_at).toLocaleString()}
                        </div>
                      </div>
                      <div className="text-blue-500 dark:text-blue-400">
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          className="h-5 w-5"
                          fill="none"
                          viewBox="0 0 24 24"
                          stroke="currentColor"
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M9 5l7 7-7 7"
                          />
                        </svg>
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              {totalHistoryItems > historyItemsPerPage && (
                <div className="mt-6">
                  <Pagination
                    currentPage={historyPage}
                    totalPages={Math.ceil(totalHistoryItems / historyItemsPerPage)}
                    onPageChange={handleHistoryPageChange}
                    itemsPerPage={historyItemsPerPage}
                    totalItems={totalHistoryItems}
                    maxVisibleButtons={5}
                    showFirstLast={true}
                  />
                </div>
              )}
            </>
          ) : (
            <div className="py-8 text-center">
              <p className="text-gray-600 dark:text-gray-400">{t('No search history found.')}</p>
              <p className="text-sm text-gray-500 dark:text-gray-500 mt-2">
                {t('Start by searching for a component above.')}
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default MarketResearchPage;
