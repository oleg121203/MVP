import React, { forwardRef } from 'react';
import './Input.css';

/**
 * Reusable Input component with support for validation states
 *
 * @param {Object} props
 * @param {string} [props.type='text'] - Input type (text, email, password, etc.)
 * @param {string} [props.label] - Input label
 * @param {string} [props.error] - Error message to display
 * @param {boolean} [props.disabled=false] - Whether the input is disabled
 * @param {string} [props.className] - Additional CSS class names
 * @param {string} [props.id] - Input id attribute
 * @param {string} [props.placeholder] - Input placeholder text
 * @param {Function} props.onChange - Change handler function
 * @param {string|number} props.value - Input value
 * @param {Object} [props.rest] - Any other props to pass to the input element
 */
const Input = forwardRef(
  (
    {
      type = 'text',
      label,
      error,
      disabled = false,
      className = '',
      id,
      placeholder,
      onChange,
      value,
      size = '', // 'small', 'large', or ''
      ...rest
    },
    ref
  ) => {
    const inputId = id || `input-${Math.random().toString(36).substring(2, 9)}`;
    const hasError = !!error;
    const sizeClass = size ? `ui-input-${size}` : '';
    const errorClass = hasError ? 'ui-input-error' : '';

    return (
      <div className="ui-input-container">
        {label && (
          <label htmlFor={inputId} className="ui-input-label">
            {label}
          </label>
        )}
        <input
          ref={ref}
          id={inputId}
          type={type}
          className={`ui-input ${sizeClass} ${errorClass} ${className}`.trim()}
          disabled={disabled}
          placeholder={placeholder}
          onChange={onChange}
          value={value}
          {...rest}
        />
        {hasError && <div className="ui-input-error-message">{error}</div>}
      </div>
    );
  }
);

Input.displayName = 'Input';

export default Input;
