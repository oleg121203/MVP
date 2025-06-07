import React from 'react';
import PropTypes from 'prop-types';
import Toast from './Toast';
import './ToastContainer.css';

const ToastContainer = ({ toasts = [], position = 'top-right', onCloseToast }) => {
  if (toasts.length === 0) {
    return null;
  }

  return (
    <div className={`toast-container ${position}`}>
      {toasts.map((toast) => (
        <Toast
          key={toast.id}
          id={toast.id}
          message={toast.message}
          type={toast.type}
          duration={toast.duration}
          icon={toast.icon}
          onClose={onCloseToast}
        />
      ))}
    </div>
  );
};

ToastContainer.propTypes = {
  toasts: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
      message: PropTypes.oneOfType([PropTypes.string, PropTypes.node]).isRequired,
      type: PropTypes.oneOf(['success', 'error', 'info', 'warning']),
      duration: PropTypes.number,
      icon: PropTypes.node,
    })
  ),
  position: PropTypes.oneOf([
    'top-right',
    'top-left',
    'bottom-right',
    'bottom-left',
    'top-center',
    'bottom-center',
  ]),
  onCloseToast: PropTypes.func.isRequired,
};

export default ToastContainer;
