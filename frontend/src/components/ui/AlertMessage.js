import React from 'react';
import './AlertMessage.css';

/**
 * Reusable AlertMessage component for displaying different types of messages
 *
 * @param {Object} props
 * @param {string} props.type - Message type (success, error, warning, info)
 * @param {string|React.ReactNode} props.message - Message content
 * @param {boolean} [props.dismissible=false] - Whether the alert can be dismissed
 * @param {Function} [props.onDismiss] - Function to call when alert is dismissed
 * @param {string} [props.className] - Additional CSS class names
 */
const AlertMessage = ({
  type = 'info',
  message,
  dismissible = false,
  onDismiss,
  className = '',
}) => {
  if (!message) return null;

  const alertClassName = `ui-alert ui-alert-${type} ${className}`.trim();

  return (
    <div className={alertClassName} role="alert">
      <div className="ui-alert-content">{message}</div>
      {dismissible && onDismiss && (
        <button type="button" className="ui-alert-close" onClick={onDismiss} aria-label="Close">
          ×
        </button>
      )}
    </div>
  );
};

export default AlertMessage;
