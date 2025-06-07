import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useToast } from '../context/ToastContext';
import {
  AlertMessage,
  Button,
  Card,
  Checkbox,
  Input,
  Modal,
  Pagination,
  SearchBar,
  Table,
  Tabs,
} from '../components/ui';
import { ConfirmationModal } from '../components/ui/Modal';
import './AdminPage.css';

// Імпортуємо API_BASE_URL з налаштувань середовища
const API_BASE_URL = process.env.REACT_APP_API_URL || '';

const AdminPage = () => {
  // Define table columns configuration for knowledge base documents
  const getDocumentColumns = (handleDelete) => [
    { header: 'ID', accessor: 'id' },
    { header: 'Source Name', accessor: 'source_name' },
    { header: 'Type', accessor: 'content_type' },
    {
      header: 'Date Added',
      accessor: 'created_at',
      cell: (row) => new Date(row.created_at).toLocaleString(),
    },
    {
      header: 'Actions',
      accessor: 'actions',
      cell: (row) => (
        <div className="action-buttons">
          <Button
            variant="secondary"
            size="small"
            className="view-button"
            onClick={() => navigate(`/admin/documents/${row.id}`)}
          >
            View
          </Button>
          <Button
            variant="danger"
            size="small"
            className="delete-button"
            onClick={() => openDeleteModal(row.id)}
          >
            Delete
          </Button>
        </div>
      ),
    },
  ];
  const { user, token } = useAuth();
  const navigate = useNavigate();
  const toast = useToast();
  const [documents, setDocuments] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage] = useState(10);
  const [totalDocuments, setTotalDocuments] = useState(0);
  const [isUploading, setIsUploading] = useState(false);
  const [isImporting, setIsImporting] = useState(false);
  const [file, setFile] = useState(null);
  const [url, setUrl] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState(null);
  // This state is kept for API calls that need the tab ID
  const [activeTab, setActiveTab] = useState('upload');
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [isSearching, setIsSearching] = useState(false);
  const [searchPage, setSearchPage] = useState(1);
  const [totalSearchResults, setTotalSearchResults] = useState(0);
  const [deleteModalOpen, setDeleteModalOpen] = useState(false);
  const [documentToDelete, setDocumentToDelete] = useState(null);

  // Market Price Sources states
  const [marketPriceSources, setMarketPriceSources] = useState([]);
  const [marketPriceSourcesPage, setMarketPriceSourcesPage] = useState(1);
  const [totalMarketPriceSources, setTotalMarketPriceSources] = useState(0);
  const [isLoadingMarketPriceSources, setIsLoadingMarketPriceSources] = useState(false);
  const [marketPriceSourceModalOpen, setMarketPriceSourceModalOpen] = useState(false);
  const [currentMarketPriceSource, setCurrentMarketPriceSource] = useState(null);
  const [deleteMarketPriceSourceModalOpen, setDeleteMarketPriceSourceModalOpen] = useState(false);
  const [marketPriceSourceToDelete, setMarketPriceSourceToDelete] = useState(null);
  const [marketPriceSourceFormData, setMarketPriceSourceFormData] = useState({
    name: '',
    url_pattern: '',
    is_anchor_site: false,
    priority: 1,
    is_active: true,
  });

  // Check if user is admin
  useEffect(() => {
    if (!user || !user.is_admin) {
      navigate('/');
    } else {
      fetchDocuments(currentPage);
      fetchMarketPriceSources(marketPriceSourcesPage);
    }
  }, [user, navigate]);

  // Handle page change
  const handlePageChange = (page) => {
    fetchDocuments(page);
  };

  // Fetch documents from API with pagination
  const fetchDocuments = async (page = 1) => {
    try {
      setIsLoading(true);

      const skip = (page - 1) * itemsPerPage;
      const response = await fetch(
        `${API_BASE_URL}/api/admin/knowledge-base/entries?skip=${skip}&limit=${itemsPerPage}`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (!response.ok) {
        throw new Error('Failed to fetch documents');
      }

      const data = await response.json();
      setDocuments(data.entries || []);
      setTotalDocuments(data.total || data.entries?.length || 0);
      setCurrentPage(page);
    } catch (err) {
      toast.error(`Failed to fetch documents: ${err.message}`);
      console.error('Error fetching documents:', err);
    } finally {
      setIsLoading(false);
    }
  };

  // Fetch documents when token or upload status changes
  useEffect(() => {
    if (token) {
      fetchDocuments(currentPage);
    }
  }, [token, uploadStatus, currentPage]);

  // Fetch market price sources when token or page changes
  useEffect(() => {
    if (token) {
      fetchMarketPriceSources(marketPriceSourcesPage);
    }
  }, [token, marketPriceSourcesPage]);

  // Define table columns for market price sources
  const getMarketPriceSourceColumns = () => [
    { header: 'ID', accessor: 'id' },
    { header: 'Name', accessor: 'name' },
    { header: 'URL Pattern', accessor: 'url_pattern' },
    {
      header: 'Anchor Site',
      accessor: 'is_anchor_site',
      cell: (row) => (row.is_anchor_site ? 'Yes' : 'No'),
    },
    {
      header: 'Priority',
      accessor: 'priority',
    },
    {
      header: 'Status',
      accessor: 'is_active',
      cell: (row) => (row.is_active ? 'Active' : 'Inactive'),
    },
    {
      header: 'Actions',
      accessor: 'actions',
      cell: (row) => (
        <div className="action-buttons">
          <Button
            variant="secondary"
            size="small"
            className="edit-button"
            onClick={() => openMarketPriceSourceEditModal(row)}
          >
            Edit
          </Button>
          <Button
            variant="danger"
            size="small"
            className="delete-button"
            onClick={() => openDeleteMarketPriceSourceModal(row.id)}
          >
            Delete
          </Button>
        </div>
      ),
    },
  ];

  // Fetch market price sources with pagination
  const fetchMarketPriceSources = async (page = 1) => {
    try {
      setIsLoadingMarketPriceSources(true);

      const skip = (page - 1) * itemsPerPage;
      const response = await fetch(
        `${API_BASE_URL}/api/admin/market-price-sources/?skip=${skip}&limit=${itemsPerPage}`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (!response.ok) {
        throw new Error('Failed to fetch market price sources');
      }

      const data = await response.json();
      setMarketPriceSources(data.sources || []);
      setTotalMarketPriceSources(data.total || 0);
      setMarketPriceSourcesPage(page);
    } catch (err) {
      toast.error(`Failed to fetch market price sources: ${err.message}`);
      console.error('Error fetching market price sources:', err);
    } finally {
      setIsLoadingMarketPriceSources(false);
    }
  };

  // Handle market price sources page change
  const handleMarketPriceSourcesPageChange = (page) => {
    setMarketPriceSourcesPage(page);
  };

  // Open modal for creating/editing market price source
  const openMarketPriceSourceEditModal = (source = null) => {
    if (source) {
      // Edit existing source
      setCurrentMarketPriceSource(source);
      setMarketPriceSourceFormData({
        name: source.name,
        url_pattern: source.url_pattern,
        is_anchor_site: source.is_anchor_site,
        priority: source.priority,
        is_active: source.is_active,
      });
    } else {
      // Create new source
      setCurrentMarketPriceSource(null);
      setMarketPriceSourceFormData({
        name: '',
        url_pattern: '',
        is_anchor_site: false,
        priority: 1,
        is_active: true,
      });
    }
    setMarketPriceSourceModalOpen(true);
  };

  // Handle form input changes
  const handleMarketPriceSourceInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setMarketPriceSourceFormData((prev) => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }));
  };

  // Handle numeric input changes with validation
  const handleNumericInputChange = (e) => {
    const { name, value } = e.target;
    const numValue = parseInt(value, 10);
    if (!isNaN(numValue) && numValue > 0) {
      setMarketPriceSourceFormData((prev) => ({
        ...prev,
        [name]: numValue,
      }));
    }
  };

  // Save market price source (create or update)
  const saveMarketPriceSource = async () => {
    try {
      const isEdit = !!currentMarketPriceSource;
      const url = isEdit
        ? `${API_BASE_URL}/api/admin/market-price-sources/${currentMarketPriceSource.id}`
        : `${API_BASE_URL}/api/admin/market-price-sources/`;

      const method = isEdit ? 'PUT' : 'POST';

      const response = await fetch(url, {
        method,
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(marketPriceSourceFormData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to save market price source');
      }

      const data = await response.json();
      toast.success(`Market price source ${isEdit ? 'updated' : 'created'} successfully`);
      setMarketPriceSourceModalOpen(false);
      fetchMarketPriceSources(marketPriceSourcesPage);
    } catch (err) {
      toast.error(`Failed to save market price source: ${err.message}`);
      console.error('Error saving market price source:', err);
    }
  };

  // Open delete confirmation modal
  const openDeleteMarketPriceSourceModal = (sourceId) => {
    setMarketPriceSourceToDelete(sourceId);
    setDeleteMarketPriceSourceModalOpen(true);
  };

  // Delete market price source
  const handleDeleteMarketPriceSource = async () => {
    try {
      const response = await fetch(
        `${API_BASE_URL}/api/admin/market-price-sources/${marketPriceSourceToDelete}`,
        {
          method: 'DELETE',
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (!response.ok) {
        throw new Error('Failed to delete market price source');
      }

      toast.success('Market price source deleted successfully');
      setDeleteMarketPriceSourceModalOpen(false);
      fetchMarketPriceSources(marketPriceSourcesPage);
    } catch (err) {
      toast.error(`Failed to delete market price source: ${err.message}`);
      console.error('Error deleting market price source:', err);
    }
  };

  // Handle file selection
  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setUploadStatus(null); // Clear upload status when new file is selected
  };

  // Handle URL input
  const handleUrlChange = (e) => {
    setUrl(e.target.value);
    setUploadStatus(null); // Clear upload status when URL is changed
  };

  // Handle file upload
  const handleFileUpload = async (e) => {
    e.preventDefault();

    if (!file) {
      toast.warning('Please select a file to upload');
      return;
    }

    try {
      setIsUploading(true);
      setUploadStatus(null);

      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch(`${API_BASE_URL}/admin/documents/upload`, {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: formData,
      });

      const result = await response.json();

      if (!result.success) {
        throw new Error(result.message);
      }

      toast.success('File uploaded successfully');
      setUploadStatus({ type: 'success', message: 'File uploaded successfully' });
      setFile(null);

      // Reset file input
      document.getElementById('file-upload').value = '';

      // Refresh documents list
      fetchDocuments(currentPage);
    } catch (err) {
      toast.error(`Upload failed: ${err.message}`);
      setUploadStatus({ type: 'error', message: `Upload failed: ${err.message}` });
      console.error('Error uploading file:', err);
    } finally {
      setIsUploading(false);
    }
  };

  // Handle URL import
  const handleUrlImport = async (e) => {
    e.preventDefault();

    if (!url) {
      toast.warning('Please enter a URL');
      return;
    }

    try {
      setIsImporting(true);
      setUploadStatus(null);

      const response = await fetch(`${API_BASE_URL}/admin/documents/import-url`, {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url }),
      });

      const result = await response.json();

      if (!result.success) {
        throw new Error(result.message);
      }

      toast.success('URL imported successfully');
      setUploadStatus({ type: 'success', message: 'URL imported successfully' });
      setUrl('');

      // Refresh documents list
      fetchDocuments(currentPage);
    } catch (err) {
      toast.error(`URL import failed: ${err.message}`);
      setUploadStatus({ type: 'error', message: `URL import failed: ${err.message}` });
      console.error('Error importing URL:', err);
    } finally {
      setIsImporting(false);
    }
  };

  // Handle document deletion
  const openDeleteModal = (documentId) => {
    setDocumentToDelete(documentId);
    setDeleteModalOpen(true);
  };

  const handleDeleteDocument = async () => {
    if (!documentToDelete) return;

    try {
      setIsLoading(true);

      const response = await fetch(`${API_BASE_URL}/admin/documents/${documentToDelete}`, {
        method: 'DELETE',
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const result = await response.json();

      if (!result.success) {
        throw new Error(result.message);
      }

      // Update documents list after deletion
      setDocuments(documents.filter((doc) => doc.id !== documentToDelete));
      toast.success('Document deleted successfully');
    } catch (err) {
      toast.error(`Failed to delete document: ${err.message}`);
      console.error('Error deleting document:', err);
    } finally {
      setIsLoading(false);
      setDocumentToDelete(null);
      setDeleteModalOpen(false);
    }
  };

  // Handle search query change
  const handleSearchChange = (e) => {
    setSearchQuery(e.target.value);
  };

  // Handle search submission
  const handleSearch = async (searchTerm, page = 1) => {
    // If called from SearchBar component, use the passed search term
    // Otherwise, use the state value (for backward compatibility)
    const query = typeof searchTerm === 'string' ? searchTerm : searchQuery;

    // If it's an event object (from form submission), prevent default
    if (searchTerm && searchTerm.preventDefault) {
      searchTerm.preventDefault();
    }

    if (!query.trim()) {
      toast.warning('Please enter a search query');
      return;
    }

    // Update searchQuery state if it was passed from SearchBar
    if (typeof searchTerm === 'string' && searchTerm !== searchQuery) {
      setSearchQuery(searchTerm);
    }

    try {
      setIsSearching(true);

      const skip = (page - 1) * itemsPerPage;
      const response = await fetch(
        `${API_BASE_URL}/api/admin/knowledge-base/search?query=${encodeURIComponent(query)}&skip=${skip}&limit=${itemsPerPage}`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (!response.ok) {
        throw new Error('Failed to search documents');
      }

      const data = await response.json();
      setSearchResults(data.documents || data);
      setTotalSearchResults(
        data.total || data.documents?.length || (Array.isArray(data) ? data.length : 0)
      );
      setSearchPage(page);
      setActiveTab('search');

      if ((data.documents || data).length === 0) {
        toast.warning(`No results found for "${query}"`);
      } else {
        toast.success(
          `Found ${data.total || (data.documents || data).length} results for "${query}"`
        );
      }
    } catch (err) {
      toast.error(`Search failed: ${err.message}`);
      console.error('Error searching documents:', err);
    } finally {
      setIsSearching(false);
    }
  };

  // Handle search page change
  const handleSearchPageChange = (page) => {
    handleSearch(null, page);
  };

  return (
    <div className="admin-container">
      <h1>Admin Panel</h1>
      <p className="admin-welcome">Welcome, {user?.username}! You have admin privileges.</p>

      <Tabs
        tabs={[
          {
            id: 'market-price-sources',
            label: 'Market Price Sources',
            content: (
              <div className="admin-section market-price-sources">
                <div className="section-header">
                  <h3>Manage Market Price Sources</h3>
                  <Button
                    variant="primary"
                    onClick={() => openMarketPriceSourceEditModal()}
                    className="add-source-button"
                  >
                    Add New Source
                  </Button>
                </div>

                <div className="market-price-sources-list">
                  <Table
                    columns={getMarketPriceSourceColumns()}
                    data={marketPriceSources}
                    isLoading={isLoadingMarketPriceSources}
                    emptyMessage="No market price sources found."
                    className="admin-table"
                  />

                  {marketPriceSources.length > 0 && (
                    <Pagination
                      currentPage={marketPriceSourcesPage}
                      totalPages={Math.ceil(totalMarketPriceSources / itemsPerPage)}
                      onPageChange={handleMarketPriceSourcesPageChange}
                      itemsPerPage={itemsPerPage}
                      totalItems={totalMarketPriceSources}
                      maxVisibleButtons={5}
                      showFirstLast={true}
                      className="admin-pagination"
                    />
                  )}
                </div>
              </div>
            ),
          },
          {
            id: 'upload',
            label: 'Upload Documents',
            content: (
              <div className="upload-section">
                <h2>Upload New Document</h2>
                <div className="upload-methods">
                  <div className="file-upload-section">
                    <h3>File Upload</h3>
                    <form onSubmit={handleFileUpload}>
                      <div className="form-group">
                        <Input
                          type="file"
                          onChange={handleFileChange}
                          label="Select a file"
                          className="file-input"
                        />
                      </div>
                      <Button
                        type="submit"
                        variant="primary"
                        isLoading={isUploading}
                        disabled={!file}
                      >
                        {isUploading ? 'Uploading...' : 'Upload'}
                      </Button>
                    </form>
                  </div>

                  <div className="url-import-section">
                    <h3>Import from URL</h3>
                    <form onSubmit={handleUrlImport}>
                      <div className="form-group">
                        <Input
                          type="text"
                          value={url}
                          onChange={(e) => setUrl(e.target.value)}
                          placeholder="https://example.com/document"
                          label="Document URL"
                        />
                      </div>
                      <Button
                        type="submit"
                        variant="primary"
                        isLoading={isImporting}
                        disabled={!url}
                      >
                        {isImporting ? 'Importing...' : 'Import'}
                      </Button>
                    </form>
                  </div>
                </div>

                {uploadStatus && (
                  <div className="upload-status">
                    <AlertMessage
                      type={uploadStatus.type || (uploadStatus.success ? 'success' : 'error')}
                      message={uploadStatus.message}
                    />
                  </div>
                )}
              </div>
            ),
          },
          {
            id: 'manage',
            label: 'Manage Knowledge Base',
            content: (
              <div className="manage-section">
                <h2>Knowledge Base Documents</h2>
                <div className="documents-list">
                  <Table
                    columns={getDocumentColumns()}
                    data={documents}
                    isLoading={isLoading}
                    emptyMessage="No documents found in the knowledge base."
                    className="admin-documents-table"
                  />

                  <Pagination
                    currentPage={currentPage}
                    totalPages={Math.ceil(totalDocuments / itemsPerPage)}
                    onPageChange={handlePageChange}
                    itemsPerPage={itemsPerPage}
                    totalItems={totalDocuments}
                    maxVisibleButtons={5}
                    showFirstLast={true}
                    className="admin-pagination"
                  />
                </div>
              </div>
            ),
          },
          {
            id: 'search',
            label: 'Search Documents',
            content: (
              <div className="search-section">
                <h2>Search Documents</h2>
                <div className="search-form-container">
                  <SearchBar
                    placeholder="Enter search terms..."
                    value={searchQuery}
                    onSearch={handleSearch}
                    isLoading={isSearching}
                    buttonText="Search"
                    showClearButton={true}
                    autoFocus={true}
                    className="admin-search-bar"
                  />
                </div>

                <div className="search-results">
                  <h3>
                    {searchResults.length > 0 && !isSearching
                      ? `Search Results (${searchResults.length})`
                      : 'Search Results'}
                  </h3>
                  <div className="documents-list">
                    <Table
                      columns={getDocumentColumns()}
                      data={searchResults}
                      isLoading={isSearching}
                      emptyMessage={
                        searchQuery
                          ? 'No documents found matching your search criteria.'
                          : 'Enter a search query above.'
                      }
                      className="admin-search-table"
                    />

                    {searchResults.length > 0 && (
                      <Pagination
                        currentPage={searchPage}
                        totalPages={Math.ceil(totalSearchResults / itemsPerPage)}
                        onPageChange={handleSearchPageChange}
                        itemsPerPage={itemsPerPage}
                        totalItems={totalSearchResults}
                        maxVisibleButtons={5}
                        showFirstLast={true}
                        className="admin-pagination"
                      />
                    )}
                  </div>
                </div>
              </div>
            ),
          },
        ]}
        defaultActiveTabId={activeTab}
        onTabChange={setActiveTab}
        className="admin-tabs"
      />
      <div className="admin-section ollama-config-info">
        <h3>Local AI (Ollama) Connection Configuration</h3>
        <p>
          The current Ollama server address for fallback requests is read from the
          <code>OLLAMA_BASE_URL</code> variable in your backend's <code>.env</code> file. The model
          is set through <code>OLLAMA_MODEL_NAME</code>.
        </p>
        <p>Configure these variables according to your environment:</p>

        <h4>Scenario 1: Backend (FastAPI) and Ollama on Same Host Machine (Not in Docker)</h4>
        <ul>
          <li>Ensure Ollama is running.</li>
          <li>
            In your backend's <code>.env</code> file, set:
            <br />
            <code>OLLAMA_BASE_URL=http://localhost:11434</code>
          </li>
          <li>
            (If backend and Ollama are on different machines in the same local network, replace{' '}
            <code>localhost</code> with the Ollama machine's IP, e.g.,{' '}
            <code>http://192.168.1.10:11434</code>)
          </li>
        </ul>

        <h4>Scenario 2: Backend in Docker Container, Ollama on Host Machine</h4>
        <ul>
          <li>
            If your FastAPI backend runs inside a Docker container and Ollama runs on the same
            machine hosting Docker:
          </li>
          <li>
            In your backend's <code>.env</code> file, set:
            <br />
            <code>OLLAMA_BASE_URL=http://host.docker.internal:11434</code>
          </li>
          <li>
            (<code>host.docker.internal</code> is a special DNS address pointing from container to
            host machine. Requires Docker Desktop 18.03+ or appropriate Docker network
            configuration).
          </li>
        </ul>

        <h4>Scenario 3: Backend and Ollama on Different Servers (External IP)</h4>
        <ul>
          <li>If Ollama runs on a separate server accessible via external IP or domain:</li>
          <li>
            In your backend's <code>.env</code> file, set:
            <br />
            <code>OLLAMA_BASE_URL=http://&lt;OLLAMA_SERVER_EXTERNAL_IP_OR_DOMAIN&gt;:11434</code>
          </li>
          <li>
            Ensure the firewall on the Ollama server allows incoming connections on port 11434 from
            your backend server's IP.
          </li>
        </ul>
        <p className="important-note">
          <strong>Important:</strong> After any changes to the <code>.env</code> file, the backend
          server must be <strong>restarted</strong> for new settings to take effect.
        </p>
      </div>

      {/* Confirmation Modal for document deletion */}
      <ConfirmationModal
        isOpen={deleteModalOpen}
        onClose={() => setDeleteModalOpen(false)}
        title="Confirm Deletion"
        message="Are you sure you want to delete this document? This action cannot be undone."
        confirmText="Delete"
        cancelText="Cancel"
        onConfirm={handleDeleteDocument}
        confirmVariant="danger"
      />

      {/* Modal for creating/editing market price sources */}
      <Modal
        isOpen={marketPriceSourceModalOpen}
        onClose={() => setMarketPriceSourceModalOpen(false)}
        title={currentMarketPriceSource ? 'Edit Market Price Source' : 'Add Market Price Source'}
        footer={
          <div className="modal-footer">
            <Button variant="secondary" onClick={() => setMarketPriceSourceModalOpen(false)}>
              Cancel
            </Button>
            <Button variant="primary" onClick={saveMarketPriceSource}>
              {currentMarketPriceSource ? 'Update' : 'Create'}
            </Button>
          </div>
        }
      >
        <div className="market-price-source-form">
          <div className="form-group">
            <label htmlFor="name">Name</label>
            <Input
              id="name"
              name="name"
              value={marketPriceSourceFormData.name}
              onChange={handleMarketPriceSourceInputChange}
              placeholder="Enter source name"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="url_pattern">URL Pattern</label>
            <Input
              id="url_pattern"
              name="url_pattern"
              value={marketPriceSourceFormData.url_pattern}
              onChange={handleMarketPriceSourceInputChange}
              placeholder="Enter URL pattern (e.g., https://example.com/products/{query})"
              required
            />
            <small className="form-text text-muted">
              Use {'{query}'} as a placeholder for search terms in the URL pattern.
            </small>
          </div>

          <div className="form-group">
            <label htmlFor="priority">Priority (1-10)</label>
            <Input
              id="priority"
              name="priority"
              type="number"
              min="1"
              max="10"
              value={marketPriceSourceFormData.priority}
              onChange={handleNumericInputChange}
              required
            />
            <small className="form-text text-muted">
              Higher priority sources are queried first (1 is lowest, 10 is highest).
            </small>
          </div>

          <div className="form-group checkbox-group">
            <Checkbox
              id="is_anchor_site"
              name="is_anchor_site"
              checked={marketPriceSourceFormData.is_anchor_site}
              onChange={handleMarketPriceSourceInputChange}
              label="Is Anchor Site"
            />
            <small className="form-text text-muted">
              Anchor sites are considered more reliable for base pricing information.
            </small>
          </div>

          <div className="form-group checkbox-group">
            <Checkbox
              id="is_active"
              name="is_active"
              checked={marketPriceSourceFormData.is_active}
              onChange={handleMarketPriceSourceInputChange}
              label="Active"
            />
            <small className="form-text text-muted">
              Only active sources will be used for market price research.
            </small>
          </div>
        </div>
      </Modal>

      {/* Confirmation Modal for market price source deletion */}
      <ConfirmationModal
        isOpen={deleteMarketPriceSourceModalOpen}
        onClose={() => setDeleteMarketPriceSourceModalOpen(false)}
        title="Confirm Deletion"
        message="Are you sure you want to delete this market price source? This action cannot be undone."
        confirmText="Delete"
        cancelText="Cancel"
        onConfirm={handleDeleteMarketPriceSource}
        confirmVariant="danger"
      />
    </div>
  );
};

export default AdminPage;
