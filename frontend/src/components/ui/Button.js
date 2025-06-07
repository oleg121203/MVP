import React from 'react';
import './Button.css';

/**
 * Reusable Button component with support for different variants and states
 *
 * @param {Object} props
 * @param {string} [props.variant='primary'] - Button variant (primary, secondary, danger)
 * @param {boolean} [props.isLoading=false] - Whether the button is in loading state
 * @param {boolean} [props.disabled=false] - Whether the button is disabled
 * @param {string} [props.className] - Additional CSS class names
 * @param {Function} props.onClick - Click handler function
 * @param {React.ReactNode} props.children - Button content
 * @param {string} [props.type='button'] - Button type attribute
 * @param {Object} [props.rest] - Any other props to pass to the button element
 */
const Button = ({
  variant = 'primary',
  isLoading = false,
  disabled = false,
  className = '',
  onClick,
  children,
  type = 'button',
  fullWidth = false,
  size = '', // 'small', 'large', or ''
  ...rest
}) => {
  const variantClass = `ui-button-${variant}`;
  const loadingClass = isLoading ? 'ui-button-loading' : '';
  const widthClass = fullWidth ? 'ui-button-full-width' : '';
  const sizeClass = size ? `ui-button-${size}` : '';

  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled || isLoading}
      className={`ui-button ${variantClass} ${loadingClass} ${widthClass} ${sizeClass} ${className}`.trim()}
      {...rest}
    >
      {isLoading ? <span className="ui-button-spinner" aria-label="Loading"></span> : null}
      <span>{children}</span>
    </button>
  );
};

export default Button;
