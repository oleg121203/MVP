import React from 'react';
import './FormGroup.css';

/**
 * FormGroup component for grouping form elements with labels
 * @param {Object} props - Component props
 * @param {React.ReactNode} props.children - Child components
 * @param {string} props.label - Label text
 * @param {string} props.htmlFor - ID of the input element this label is for
 * @param {string} props.className - Additional CSS class
 * @param {boolean} props.required - Whether the field is required
 * @param {string} props.error - Error message
 * @param {string} props.helpText - Help text
 */
const FormGroup = ({
  children,
  label,
  htmlFor,
  className = '',
  required = false,
  error = '',
  helpText = '',
}) => {
  return (
    <div className={`form-group ${className} ${error ? 'has-error' : ''}`}>
      {label && (
        <label htmlFor={htmlFor} className="form-label">
          {label}
          {required && <span className="required-indicator">*</span>}
        </label>
      )}
      {children}
      {helpText && <div className="help-text">{helpText}</div>}
      {error && <div className="error-message">{error}</div>}
    </div>
  );
};

export default FormGroup;
