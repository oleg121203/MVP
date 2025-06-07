import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  getProjectDetails,
  runComplianceCheckForProject,
  runOptimizationAnalysisForProject,
  analyzeDocument,
  refineAnalysis,
  generateCommercialProposalForProject,
  getSpecificationsByProject,
  createSpecification,
  updateSpecification,
  deleteSpecification,
  searchSpecifications,
} from '../services/apiService';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';
import { useLocalization } from '../context/LocalizationContext';
import { useToast } from '../context/ToastContext';
import { Button } from '../components/ui';
import SpecificationFormModal from '../components/SpecificationFormModal';
import ProjectChatInterface from '../components/ProjectChatInterface';
import ProjectAnalysisWizard from '../components/ProjectAnalysisWizard';
import {
  FaChevronDown,
  FaChevronRight,
  FaCheckCircle,
  FaTimesCircle,
  FaExclamationTriangle,
  FaFileDownload,
  FaSearch,
  FaTools,
} from 'react-icons/fa';

// Inline styles
const styles = {
  container: {
    maxWidth: '1200px',
    margin: '0 auto',
    padding: '20px',
    fontFamily: 'Arial, sans-serif',
  },
  card: {
    backgroundColor: 'var(--card-bg-light, #ffffff)',
    borderRadius: '8px',
    boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)',
    padding: '20px',
    marginBottom: '24px',
    border: '1px solid var(--border-light, #e2e8f0)',
  },
  heading: {
    fontSize: '1.875rem',
    fontWeight: '700',
    marginBottom: '0.75rem',
  },
  description: {
    fontSize: '1rem',
    marginBottom: '1.5rem',
    color: 'var(--text-color, #4b5563)',
  },
  sectionHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    cursor: 'pointer',
    padding: '10px 0',
    borderBottom: '1px solid var(--border-light, #e5e7eb)',
    marginBottom: '15px',
  },
  sectionHeading: {
    fontSize: '1.25rem',
    fontWeight: '600',
    margin: 0,
  },
  button: {
    backgroundColor: 'var(--primary-color, #2563eb)',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    padding: '8px 16px',
    cursor: 'pointer',
    display: 'inline-flex',
    alignItems: 'center',
    gap: '8px',
    fontSize: '0.9rem',
  },
  buttonDisabled: {
    backgroundColor: 'var(--disabled-light, #9ca3af)',
    cursor: 'not-allowed',
  },
  table: {
    width: '100%',
    borderCollapse: 'collapse',
    marginTop: '15px',
    border: '1px solid var(--border-light, #e2e8f0)',
  },
  th: {
    backgroundColor: 'var(--table-header-bg-light, #f8f9fa)',
    padding: '12px',
    textAlign: 'left',
    borderBottom: '1px solid var(--border-light, #e5e7eb)',
    fontWeight: '600',
    fontSize: '0.75rem',
    textTransform: 'uppercase',
  },
  td: {
    padding: '12px',
    borderBottom: '1px solid var(--border-light, #e5e7eb)',
    verticalAlign: 'top',
    fontSize: '0.875rem',
  },
  compliant: {
    color: 'var(--success-light, #10b981)',
    display: 'flex',
    alignItems: 'center',
    gap: '4px',
  },
  nonCompliant: {
    color: 'var(--error-light, #ef4444)',
    display: 'flex',
    alignItems: 'center',
    gap: '4px',
  },
  warning: {
    color: 'var(--warning-light, #f59e0b)',
    display: 'flex',
    alignItems: 'center',
    gap: '4px',
  },
  loadingContainer: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    height: '200px',
  },
  errorContainer: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    height: '200px',
    color: 'var(--error-light, #ef4444)',
  },
  notFoundContainer: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    height: '200px',
  },
};

const ProjectDetailPage = () => {
  // Hooks and context
  const { t } = useLocalization();
  const { token } = useAuth();
  const { theme } = useTheme();
  const { success, error, warning, info } = useToast();
  const { id } = useParams();
  const navigate = useNavigate();
  const fileInputRef = useRef(null);

  // Project state
  const [project, setProject] = useState(null);
  const [loading, setLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState('');

  // Specification state
  const [specifications, setSpecifications] = useState([]);
  const [isLoadingSpecifications, setIsLoadingSpecifications] = useState(false);
  const [editingSpecification, setEditingSpecification] = useState(null);
  const [showSpecificationModal, setShowSpecificationModal] = useState(false);
  const [specificationSearchTerm, setSpecificationSearchTerm] = useState('');
  const [searchedSpecifications, setSearchedSpecifications] = useState([]);

  // Analysis state
  const [complianceReport, setComplianceReport] = useState(null);
  const [optimizationReport, setOptimizationReport] = useState(null);
  const [commercialProposal, setCommercialProposal] = useState(null);
  const [isChecking, setIsChecking] = useState(false);
  const [isOptimizing, setIsOptimizing] = useState(false);
  const [isGeneratingProposal, setIsGeneratingProposal] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [analysisSession, setAnalysisSession] = useState(null);
  const [analysisQuestions, setAnalysisQuestions] = useState([]);
  const [isAnalysisWizardOpen, setIsAnalysisWizardOpen] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  // UI state
  const [expandedSections, setExpandedSections] = useState({
    compliance: false,
    optimization: false,
    proposal: false,
    extractedSpecs: false,
  });

  // Dynamic theming
  const themedStyles = {
    ...styles,
    card: {
      ...styles.card,
      backgroundColor: theme === 'dark' ? '#1e293b' : '#ffffff',
      border: `1px solid ${theme === 'dark' ? '#334155' : '#e2e8f0'}`,
    },
    table: {
      ...styles.table,
      border: `1px solid ${theme === 'dark' ? '#334155' : '#e2e8f0'}`,
    },
    th: {
      ...styles.th,
      backgroundColor: theme === 'dark' ? '#334155' : '#f8f9fa',
      color: theme === 'dark' ? '#f1f5f9' : '#374151',
      borderBottom: `1px solid ${theme === 'dark' ? '#475569' : '#e5e7eb'}`,
    },
    td: {
      ...styles.td,
      color: theme === 'dark' ? '#e2e8f0' : '#374151',
      borderBottom: `1px solid ${theme === 'dark' ? '#334155' : '#e5e7eb'}`,
    },
  };

  // Toggle section expansion
  const toggleSection = (section) => {
    setExpandedSections((prev) => ({
      ...prev,
      [section]: !prev[section],
    }));
  };

  // Fetch project details on component mount
  useEffect(() => {
    const fetchProjectDetails = async () => {
      if (!id) {
        setErrorMessage(t('Invalid project ID'));
        setLoading(false);
        return;
      }

      try {
        setLoading(true);
        const projectData = await getProjectDetails(id);
        setProject(projectData);
        setErrorMessage('');
      } catch (err) {
        console.error('Error fetching project details:', err);
        setErrorMessage(err.message || t('Failed to fetch project details'));
      } finally {
        setLoading(false);
      }
    };

    fetchProjectDetails();
  }, [id, t]);

  // Fetch specifications when project id changes
  useEffect(() => {
    if (!id) return;
    fetchSpecifications();
  }, [id]);

  // Fetch specifications helper
  const fetchSpecifications = async () => {
    setIsLoadingSpecifications(true);
    try {
      const specs = await getSpecificationsByProject(id);
      setSpecifications(specs);
      setSearchedSpecifications([]);
    } catch (err) {
      error(t('Failed to fetch specifications: ') + (err.message || t('Unknown error')));
    } finally {
      setIsLoadingSpecifications(false);
    }
  };

  // Create specification
  const handleCreateSpecification = () => {
    setEditingSpecification(null);
    setShowSpecificationModal(true);
  };

  // Edit specification
  const handleEditSpecification = (spec) => {
    setEditingSpecification(spec);
    setShowSpecificationModal(true);
  };

  // Save specification (create or update)
  const handleSaveSpecification = async (specData) => {
    try {
      if (editingSpecification) {
        await updateSpecification(editingSpecification.id, specData);
        success(t('Specification updated successfully'));
      } else {
        await createSpecification(id, specData);
        success(t('Specification created successfully'));
      }
      setShowSpecificationModal(false);
      setEditingSpecification(null);
      fetchSpecifications();
    } catch (err) {
      error(t('Failed to save specification: ') + (err.message || t('Unknown error')));
    }
  };

  // Delete specification
  const handleDeleteSpecification = async (specId) => {
    if (!window.confirm(t('Are you sure you want to delete this specification?'))) return;
    try {
      await deleteSpecification(specId);
      success(t('Specification deleted successfully'));
      fetchSpecifications();
    } catch (err) {
      error(t('Failed to delete specification: ') + (err.message || t('Unknown error')));
    }
  };

  // Search specifications
  const handleSearchSpecifications = async () => {
    if (!specificationSearchTerm) return;
    setIsLoadingSpecifications(true);
    try {
      const results = await searchSpecifications(id, specificationSearchTerm);
      setSearchedSpecifications(results);
    } catch (err) {
      error(t('Failed to search specifications: ') + (err.message || t('Unknown error')));
    } finally {
      setIsLoadingSpecifications(false);
    }
  };

  // Close specification modal
  const handleCloseSpecificationModal = () => {
    setShowSpecificationModal(false);
    setEditingSpecification(null);
  };

  // Handle compliance check
  const handleComplianceCheck = async () => {
    setIsChecking(true);
    try {
      const complianceData = await runComplianceCheckForProject(id);
      setComplianceReport(complianceData);
      setExpandedSections((prev) => ({ ...prev, compliance: true }));
      success(t('Compliance check completed successfully'));
    } catch (err) {
      error(t('Failed to run compliance check: ') + (err.message || t('Unknown error')));
    } finally {
      setIsChecking(false);
    }
  };

  // Handle optimization analysis
  const handleOptimizationAnalysis = async () => {
    setIsOptimizing(true);
    try {
      const optimizationData = await runOptimizationAnalysisForProject(id);
      setOptimizationReport(optimizationData);
      setExpandedSections((prev) => ({ ...prev, optimization: true }));
      success(t('Optimization analysis completed successfully'));
    } catch (err) {
      error(t('Failed to run optimization analysis: ') + (err.message || t('Unknown error')));
    } finally {
      setIsOptimizing(false);
    }
  };

  // Handle commercial proposal generation
  const handleGenerateProposal = async () => {
    setIsGeneratingProposal(true);
    try {
      const proposalData = await generateCommercialProposalForProject(id);
      setCommercialProposal(proposalData);
      setExpandedSections((prev) => ({ ...prev, proposal: true }));
      success(t('Commercial proposal generated successfully'));
    } catch (err) {
      error(t('Failed to generate commercial proposal: ') + (err.message || t('Unknown error')));
    } finally {
      setIsGeneratingProposal(false);
    }
  };

  // Handle file selection
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (!file) return;

    // Validate file type
    const validTypes = [
      'application/pdf',
      'application/msword',
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
      'image/jpeg',
      'image/png',
      'text/plain',
    ];

    if (!validTypes.includes(file.type)) {
      error(t('Invalid file type. Please upload a PDF, Word document, or image file.'));
      return;
    }

    // Check file size (max 10MB)
    if (file.size > 10 * 1024 * 1024) {
      error(t('File size exceeds 10MB limit'));
      return;
    }

    setSelectedFile(file);
  };

  // Handle file upload and analysis
  const handleUploadAndAnalyze = async () => {
    if (!selectedFile) {
      warning(t('Please select a file to upload'));
      return;
    }

    try {
      setIsUploading(true);

      // Create FormData and append the file
      const formData = new FormData();
      formData.append('file', selectedFile);
      formData.append('project_id', id);

      // Call the API to upload and analyze the document
      const response = await analyzeDocument(formData);

      if (response.session_id) {
        setAnalysisSession({
          id: response.session_id,
          document_name: selectedFile.name,
          status: 'in_progress',
        });

        if (response.questions && response.questions.length > 0) {
          setAnalysisQuestions(response.questions);
          setIsAnalysisWizardOpen(true);
        } else {
          // No questions, show the result directly
          setAnalysisResult(response.result);
          success(t('Document analyzed successfully!'));
        }
      }

      // Clear the file input
      setSelectedFile(null);
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    } catch (err) {
      console.error('Error analyzing document:', err);
      error(err.message || t('Failed to analyze document'));
    } finally {
      setIsUploading(false);
    }
  };

  // Handle analysis wizard submission
  const handleAnalysisSubmit = async (answers) => {
    try {
      setIsAnalyzing(true);

      // Submit answers to the backend
      const response = await refineAnalysis({
        session_id: analysisSession.id,
        answers: answers,
      });

      if (response.complete) {
        // Analysis is complete
        setAnalysisResult(response.result);
        setAnalysisQuestions([]);
        setIsAnalysisWizardOpen(false);
        success(t('Analysis completed successfully!'));

        // Refresh project data to get updated specifications
        const updatedProject = await getProjectDetails(id);
        setProject(updatedProject);
      } else if (response.questions && response.questions.length > 0) {
        // More questions to answer
        setAnalysisQuestions(response.questions);
      }
    } catch (err) {
      console.error('Error submitting analysis:', err);
      error(err.message || t('Failed to process analysis'));
    } finally {
      setIsAnalyzing(false);
    }
  };

  // Handle analysis wizard close
  const handleAnalysisClose = () => {
    setIsAnalysisWizardOpen(false);
    setAnalysisQuestions([]);
  };

  // Render loading state
  if (loading && !project) {
    return (
      <div style={styles.loadingContainer}>
        <div>{t('Loading project details...')}</div>
      </div>
    );
  }

  // Render error state
  if (errorMessage) {
    return (
      <div style={styles.errorContainer}>
        <p>{errorMessage}</p>
        <Button onClick={() => window.location.reload()}>{t('Retry')}</Button>
      </div>
    );
  }

  // Render project not found
  if (!project) {
    return (
      <div style={styles.notFoundContainer}>
        <h2>{t('Project not found')}</h2>
        <p>{t('The requested project could not be found.')}</p>
        <Button onClick={() => navigate('/projects')}>{t('Back to Projects')}</Button>
      </div>
    );
  }

  return (
    <div style={styles.container}>
      {/* Project Header */}
      <div style={themedStyles.card}>
        <h1 style={styles.heading}>{project.name}</h1>
        <p style={styles.description}>{project.description}</p>

        {/* Action Buttons */}
        <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap', marginBottom: '20px' }}>
          <button
            style={{ ...styles.button, ...(isChecking ? styles.buttonDisabled : {}) }}
            onClick={handleComplianceCheck}
            disabled={isChecking}
          >
            <FaCheckCircle />
            {isChecking ? t('Checking...') : t('Run Compliance Check')}
          </button>

          <button
            style={{ ...styles.button, ...(isOptimizing ? styles.buttonDisabled : {}) }}
            onClick={handleOptimizationAnalysis}
            disabled={isOptimizing}
          >
            <FaTools />
            {isOptimizing ? t('Analyzing...') : t('Run Optimization Analysis')}
          </button>

          <button
            style={{ ...styles.button, ...(isGeneratingProposal ? styles.buttonDisabled : {}) }}
            onClick={handleGenerateProposal}
            disabled={isGeneratingProposal}
          >
            <FaFileDownload />
            {isGeneratingProposal ? t('Generating...') : t('Generate Commercial Proposal')}
          </button>
        </div>

        {/* Document Upload Section */}
        <div
          style={{
            marginTop: '20px',
            padding: '15px',
            backgroundColor: theme === 'dark' ? '#334155' : '#f8f9fa',
            borderRadius: '8px',
          }}
        >
          <h4 style={{ margin: '0 0 10px 0' }}>{t('Upload Document for Analysis')}</h4>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', flexWrap: 'wrap' }}>
            <input
              ref={fileInputRef}
              type="file"
              onChange={handleFileChange}
              accept=".pdf,.doc,.docx,.jpg,.jpeg,.png,.txt"
              style={{ flex: '1', minWidth: '200px' }}
            />
            <button
              style={{
                ...styles.button,
                ...(isUploading || !selectedFile ? styles.buttonDisabled : {}),
              }}
              onClick={handleUploadAndAnalyze}
              disabled={isUploading || !selectedFile}
            >
              {isUploading ? t('Uploading...') : t('Upload & Analyze')}
            </button>
          </div>
          <p
            style={{
              fontSize: '0.8rem',
              color: theme === 'dark' ? '#94a3b8' : '#6b7280',
              margin: '5px 0 0 0',
            }}
          >
            {t(
              'Supported formats: PDF, Word documents, images (JPG, PNG), plain text. Max size: 10MB'
            )}
          </p>
        </div>
      </div>

      {/* Compliance Report Section */}
      {complianceReport && (
        <div style={themedStyles.card}>
          <div
            style={{ ...themedStyles.sectionHeader, cursor: 'pointer' }}
            onClick={() => toggleSection('compliance')}
          >
            <h3 style={themedStyles.sectionHeading}>{t('Compliance Report')}</h3>
            <FaChevronDown
              style={{
                transform: expandedSections.compliance ? 'rotate(0deg)' : 'rotate(-90deg)',
                transition: 'transform 0.2s',
              }}
            />
          </div>
          {expandedSections.compliance && (
            <div>
              <table style={themedStyles.table}>
                <thead>
                  <tr>
                    <th style={themedStyles.th}>{t('Standard')}</th>
                    <th style={themedStyles.th}>{t('Status')}</th>
                    <th style={themedStyles.th}>{t('Notes')}</th>
                  </tr>
                </thead>
                <tbody>
                  {complianceReport.checks?.map((check, index) => (
                    <tr key={index}>
                      <td style={themedStyles.td}>{check.standard}</td>
                      <td style={themedStyles.td}>
                        <span style={check.compliant ? styles.compliant : styles.nonCompliant}>
                          {check.compliant ? <FaCheckCircle /> : <FaTimesCircle />}
                          {check.compliant ? t('Compliant') : t('Non-Compliant')}
                        </span>
                      </td>
                      <td style={themedStyles.td}>{check.notes}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}

      {/* Optimization Report Section */}
      {optimizationReport && (
        <div style={themedStyles.card}>
          <div
            style={{ ...themedStyles.sectionHeader, cursor: 'pointer' }}
            onClick={() => toggleSection('optimization')}
          >
            <h3 style={themedStyles.sectionHeading}>{t('Optimization Analysis')}</h3>
            <FaChevronDown
              style={{
                transform: expandedSections.optimization ? 'rotate(0deg)' : 'rotate(-90deg)',
                transition: 'transform 0.2s',
              }}
            />
          </div>
          {expandedSections.optimization && (
            <div>
              <table style={themedStyles.table}>
                <thead>
                  <tr>
                    <th style={themedStyles.th}>{t('Component')}</th>
                    <th style={themedStyles.th}>{t('Current')}</th>
                    <th style={themedStyles.th}>{t('Recommended')}</th>
                    <th style={themedStyles.th}>{t('Savings')}</th>
                  </tr>
                </thead>
                <tbody>
                  {optimizationReport.recommendations?.map((rec, index) => (
                    <tr key={index}>
                      <td style={themedStyles.td}>{rec.component}</td>
                      <td style={themedStyles.td}>{rec.current}</td>
                      <td style={themedStyles.td}>{rec.recommended}</td>
                      <td style={themedStyles.td}>{rec.savings}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}

      {/* Commercial Proposal Section */}
      {commercialProposal && (
        <div style={themedStyles.card}>
          <div
            style={{ ...themedStyles.sectionHeader, cursor: 'pointer' }}
            onClick={() => toggleSection('proposal')}
          >
            <h3 style={themedStyles.sectionHeading}>{t('Commercial Proposal')}</h3>
            <FaChevronDown
              style={{
                transform: expandedSections.proposal ? 'rotate(0deg)' : 'rotate(-90deg)',
                transition: 'transform 0.2s',
              }}
            />
          </div>
          {expandedSections.proposal && (
            <div>
              <div style={{ whiteSpace: 'pre-wrap', lineHeight: '1.6' }}>
                {commercialProposal.content || t('No proposal content available')}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Extracted Specifications Section */}
      {analysisResult?.specifications?.length > 0 && (
        <div style={themedStyles.card}>
          <div
            style={{ ...themedStyles.sectionHeader, cursor: 'pointer' }}
            onClick={() => toggleSection('extractedSpecs')}
          >
            <h3 style={themedStyles.sectionHeading}>{t('Extracted Specifications')}</h3>
            <FaChevronDown
              style={{
                transform: expandedSections.extractedSpecs ? 'rotate(0deg)' : 'rotate(-90deg)',
                transition: 'transform 0.2s',
              }}
            />
          </div>
          {expandedSections.extractedSpecs && (
            <div>
              <table style={themedStyles.table}>
                <thead>
                  <tr>
                    <th style={themedStyles.th}>{t('Component Type')}</th>
                    <th style={themedStyles.th}>{t('Name')}</th>
                    <th style={themedStyles.th}>{t('Quantity')}</th>
                    <th style={themedStyles.th}>{t('Unit')}</th>
                    <th style={themedStyles.th}>{t('Dimensions')}</th>
                    <th style={themedStyles.th}>{t('Airflow (m³/h)')}</th>
                    <th style={themedStyles.th}>{t('Pressure (Pa)')}</th>
                    <th style={themedStyles.th}>{t('Power (kW)')}</th>
                    <th style={themedStyles.th}>{t('Noise (dBA)')}</th>
                    <th style={themedStyles.th}>{t('Voltage (V)')}</th>
                    <th style={themedStyles.th}>{t('Notes')}</th>
                  </tr>
                </thead>
                <tbody>
                  {analysisResult.specifications.map((spec, index) => (
                    <tr
                      key={index}
                      style={{
                        backgroundColor:
                          index % 2 === 0
                            ? theme === 'dark'
                              ? 'rgba(255, 255, 255, 0.02)'
                              : 'rgba(0, 0, 0, 0.01)'
                            : 'transparent',
                      }}
                    >
                      <td style={themedStyles.td}>{spec.component_type}</td>
                      <td style={themedStyles.td}>{spec.name}</td>
                      <td style={themedStyles.td}>{spec.quantity}</td>
                      <td style={themedStyles.td}>{spec.unit}</td>
                      <td style={themedStyles.td}>{JSON.stringify(spec.dimensions || {})}</td>
                      <td style={themedStyles.td}>{spec.airflow_rate_m3h}</td>
                      <td style={themedStyles.td}>{spec.pressure_pa}</td>
                      <td style={themedStyles.td}>{spec.power_kw}</td>
                      <td style={themedStyles.td}>{spec.noise_level_db}</td>
                      <td style={themedStyles.td}>{spec.voltage_v}</td>
                      <td style={themedStyles.td}>{spec.notes}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
              <p
                style={{
                  marginTop: '16px',
                  fontSize: '0.875rem',
                  color: theme === 'dark' ? '#9ca3af' : '#6b7280',
                }}
              >
                {t('These specifications have been extracted and saved to your project.')}
              </p>
            </div>
          )}
        </div>
      )}

      {/* Specifications Section */}
      <div style={themedStyles.card}>
        <div style={themedStyles.sectionHeader}>
          <h3 style={themedStyles.sectionHeading}>{t('Specifications')}</h3>
          <div style={{ display: 'flex', gap: '8px' }}>
            <input
              type="text"
              placeholder={t('Search specifications...')}
              value={specificationSearchTerm}
              onChange={(e) => setSpecificationSearchTerm(e.target.value)}
              style={{
                padding: '6px',
                borderRadius: '4px',
                border: '1px solid #e5e7eb',
                marginRight: '8px',
                backgroundColor: theme === 'dark' ? '#334155' : '#ffffff',
                color: theme === 'dark' ? '#f1f5f9' : '#374151',
              }}
              onKeyDown={(e) => e.key === 'Enter' && handleSearchSpecifications()}
            />
            <button
              style={styles.button}
              onClick={handleSearchSpecifications}
              disabled={!specificationSearchTerm}
            >
              <FaSearch style={{ marginRight: '6px' }} />
              {t('Search')}
            </button>
            <button style={styles.button} onClick={handleCreateSpecification}>
              + {t('Add Specification')}
            </button>
          </div>
        </div>
        {isLoadingSpecifications ? (
          <div>{t('Loading specifications...')}</div>
        ) : (
          <table style={themedStyles.table}>
            <thead>
              <tr>
                <th style={themedStyles.th}>{t('Component Type')}</th>
                <th style={themedStyles.th}>{t('Name')}</th>
                <th style={themedStyles.th}>{t('Quantity')}</th>
                <th style={themedStyles.th}>{t('Unit')}</th>
                <th style={themedStyles.th}>{t('Dimensions')}</th>
                <th style={themedStyles.th}>{t('Notes')}</th>
                <th style={themedStyles.th}>{t('Actions')}</th>
              </tr>
            </thead>
            <tbody>
              {(specificationSearchTerm && searchedSpecifications.length > 0
                ? searchedSpecifications
                : specifications
              ).map((spec, idx) => (
                <tr key={spec.id || idx}>
                  <td style={themedStyles.td}>{spec.component_type}</td>
                  <td style={themedStyles.td}>{spec.name}</td>
                  <td style={themedStyles.td}>{spec.quantity}</td>
                  <td style={themedStyles.td}>{spec.unit}</td>
                  <td style={themedStyles.td}>{JSON.stringify(spec.dimensions || {})}</td>
                  <td style={themedStyles.td}>{spec.notes}</td>
                  <td style={themedStyles.td}>
                    <button
                      style={{ ...styles.button, marginRight: '4px' }}
                      onClick={() => handleEditSpecification(spec)}
                    >
                      {t('Edit')}
                    </button>
                    <button
                      style={{ ...styles.button, backgroundColor: '#ef4444' }}
                      onClick={() => handleDeleteSpecification(spec.id)}
                    >
                      {t('Delete')}
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {/* Specification Modal */}
      {showSpecificationModal && (
        <SpecificationFormModal
          show={showSpecificationModal}
          onClose={handleCloseSpecificationModal}
          onSave={handleSaveSpecification}
          specification={editingSpecification}
        />
      )}

      {/* Analysis Wizard */}
      <ProjectAnalysisWizard
        isOpen={isAnalysisWizardOpen}
        onClose={handleAnalysisClose}
        onSubmit={handleAnalysisSubmit}
        questions={analysisQuestions}
        isAnalyzing={isAnalyzing}
        sessionId={analysisSession?.id}
      />

      {/* Project Chat Section */}
      <ProjectChatInterface projectId={id} />
    </div>
  );
};

export default ProjectDetailPage;
