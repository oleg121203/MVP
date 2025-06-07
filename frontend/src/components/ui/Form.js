import React from 'react';
import AlertMessage from './AlertMessage';
import './Form.css';

/**
 * Form component for standardizing form layout, styling, and behavior
 *
 * @param {Object} props - Component props
 * @param {React.ReactNode} props.children - Form fields and content
 * @param {Function} props.onSubmit - Form submission handler
 * @param {string} [props.className] - Additional CSS classes
 * @param {string} [props.title] - Form title displayed at the top
 * @param {string|React.ReactNode} [props.error] - Error message or component to display
 * @param {React.ReactNode} [props.actions] - Form actions (usually buttons) displayed at the bottom
 * @param {boolean} [props.fullWidth=false] - Whether the form should take full width of its container
 * @returns {JSX.Element} Form component
 */
const Form = ({ children, onSubmit, className = '', title, error, actions, fullWidth = false }) => {
  const handleSubmit = (event) => {
    event.preventDefault();
    if (onSubmit) {
      onSubmit(event);
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      className={`custom-form ${fullWidth ? 'full-width' : ''} ${className}`}
      noValidate // Disable browser's native validation to use custom validation
    >
      {title && <h2 className="form-title">{title}</h2>}

      {error && (
        <div className="form-error">
          {typeof error === 'string' ? <AlertMessage type="error" message={error} /> : error}
        </div>
      )}

      <div className="form-fields">{children}</div>

      {actions && <div className="form-actions">{actions}</div>}
    </form>
  );
};

/**
 * FormGroup component for grouping related form fields
 *
 * @param {Object} props - Component props
 * @param {React.ReactNode} props.children - Form fields to group
 * @param {string} [props.className] - Additional CSS classes
 * @param {string} [props.label] - Group label
 * @returns {JSX.Element} FormGroup component
 */
export const FormGroup = ({ children, className = '', label }) => {
  return (
    <div className={`form-group ${className}`}>
      {label && <label className="form-group-label">{label}</label>}
      {children}
    </div>
  );
};

export default Form;
