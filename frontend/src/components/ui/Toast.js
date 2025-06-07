import React, { useEffect, useState } from 'react';
import PropTypes from 'prop-types';
import './Toast.css';

const Toast = ({ id, message, type = 'info', duration = 5000, onClose, icon }) => {
  const [isVisible, setIsVisible] = useState(true);

  useEffect(() => {
    if (duration) {
      const timer = setTimeout(() => {
        setIsVisible(false);
        setTimeout(() => onClose(id), 300); // Allow animation to complete before removing
      }, duration);

      return () => clearTimeout(timer);
    }
  }, [duration, id, onClose]);

  const handleClose = () => {
    setIsVisible(false);
    setTimeout(() => onClose(id), 300); // Allow animation to complete before removing
  };

  const getDefaultIcon = () => {
    switch (type) {
      case 'success':
        return <span className="toast-icon success">✓</span>;
      case 'error':
        return <span className="toast-icon error">✕</span>;
      case 'warning':
        return <span className="toast-icon warning">!</span>;
      case 'info':
      default:
        return <span className="toast-icon info">i</span>;
    }
  };

  return (
    <div className={`toast ${type} ${isVisible ? 'visible' : 'hidden'}`}>
      <div className="toast-content">
        {icon || getDefaultIcon()}
        <div className="toast-message">{message}</div>
      </div>
      <button className="toast-close" onClick={handleClose}>
        ✕
      </button>
    </div>
  );
};

Toast.propTypes = {
  id: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
  message: PropTypes.oneOfType([PropTypes.string, PropTypes.node]).isRequired,
  type: PropTypes.oneOf(['success', 'error', 'info', 'warning']),
  duration: PropTypes.number,
  onClose: PropTypes.func.isRequired,
  icon: PropTypes.node,
};

export default Toast;
