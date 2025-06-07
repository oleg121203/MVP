import React from 'react';
import { useTheme } from '../../context/ThemeContext';

/**
 * Checkbox component with theme support
 * @param {Object} props - Component props
 * @param {string} props.id - Unique identifier for the checkbox
 * @param {string} props.label - Label text for the checkbox
 * @param {boolean} props.checked - Whether the checkbox is checked
 * @param {function} props.onChange - Function to call when checkbox state changes
 * @param {boolean} props.disabled - Whether the checkbox is disabled
 * @param {string} props.className - Additional CSS classes
 */
const Checkbox = ({
  id,
  label,
  checked = false,
  onChange,
  disabled = false,
  className = '',
  ...rest
}) => {
  const { theme } = useTheme();
  const isDark = theme === 'dark';

  const styles = {
    container: {
      display: 'flex',
      alignItems: 'center',
      marginBottom: '8px',
      cursor: disabled ? 'not-allowed' : 'pointer',
      opacity: disabled ? 0.6 : 1,
    },
    checkbox: {
      appearance: 'none',
      width: '18px',
      height: '18px',
      border: `2px solid ${isDark ? '#6c757d' : '#495057'}`,
      borderRadius: '3px',
      marginRight: '8px',
      position: 'relative',
      backgroundColor: 'transparent',
      cursor: disabled ? 'not-allowed' : 'pointer',
      transition: 'all 0.2s ease',
    },
    label: {
      color: isDark ? '#e9ecef' : '#212529',
      fontSize: '14px',
      userSelect: 'none',
    },
    checkedStyle: {
      backgroundColor: isDark ? '#0d6efd' : '#0d6efd',
      borderColor: isDark ? '#0d6efd' : '#0d6efd',
    },
    checkmark: {
      position: 'absolute',
      top: '1px',
      left: '5px',
      width: '6px',
      height: '10px',
      border: 'solid white',
      borderWidth: '0 2px 2px 0',
      transform: 'rotate(45deg)',
      display: checked ? 'block' : 'none',
    },
  };

  const handleClick = () => {
    if (!disabled && onChange) {
      onChange(!checked);
    }
  };

  return (
    <div
      style={styles.container}
      className={`checkbox-container ${className}`}
      onClick={handleClick}
    >
      <div
        style={{
          ...styles.checkbox,
          ...(checked ? styles.checkedStyle : {}),
        }}
      >
        <div style={styles.checkmark}></div>
      </div>
      <input
        type="checkbox"
        id={id}
        checked={checked}
        onChange={(e) => onChange && onChange(e.target.checked)}
        disabled={disabled}
        style={{ display: 'none' }}
        {...rest}
      />
      {label && (
        <label htmlFor={id} style={styles.label}>
          {label}
        </label>
      )}
    </div>
  );
};

export default Checkbox;
