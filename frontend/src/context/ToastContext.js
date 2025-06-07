import React, { createContext, useContext, useReducer, useCallback } from 'react';
import PropTypes from 'prop-types';
import ToastContainer from '../components/ui/ToastContainer';

// Create context
const ToastContext = createContext();

// Toast reducer
const toastReducer = (state, action) => {
  switch (action.type) {
    case 'ADD_TOAST':
      return [...state, action.payload];
    case 'REMOVE_TOAST':
      return state.filter((toast) => toast.id !== action.payload);
    default:
      return state;
  }
};

// Toast provider component
export const ToastProvider = ({ children, position = 'top-right' }) => {
  const [toasts, dispatch] = useReducer(toastReducer, []);

  // Generate unique ID for each toast
  const generateId = () => {
    return Date.now().toString(36) + Math.random().toString(36).substr(2, 5);
  };

  // Add a new toast
  const addToast = useCallback((message, type = 'info', duration = 5000, icon = null) => {
    const id = generateId();
    dispatch({
      type: 'ADD_TOAST',
      payload: { id, message, type, duration, icon },
    });
    return id;
  }, []);

  // Remove a toast by ID
  const removeToast = useCallback((id) => {
    dispatch({
      type: 'REMOVE_TOAST',
      payload: id,
    });
  }, []);

  // Convenience methods for different toast types
  const success = useCallback(
    (message, duration, icon) => addToast(message, 'success', duration, icon),
    [addToast]
  );

  const error = useCallback(
    (message, duration, icon) => addToast(message, 'error', duration, icon),
    [addToast]
  );

  const info = useCallback(
    (message, duration, icon) => addToast(message, 'info', duration, icon),
    [addToast]
  );

  const warning = useCallback(
    (message, duration, icon) => addToast(message, 'warning', duration, icon),
    [addToast]
  );

  return (
    <ToastContext.Provider
      value={{
        addToast,
        removeToast,
        success,
        error,
        info,
        warning,
      }}
    >
      {children}
      <ToastContainer toasts={toasts} position={position} onCloseToast={removeToast} />
    </ToastContext.Provider>
  );
};

ToastProvider.propTypes = {
  children: PropTypes.node.isRequired,
  position: PropTypes.oneOf([
    'top-right',
    'top-left',
    'bottom-right',
    'bottom-left',
    'top-center',
    'bottom-center',
  ]),
};

// Custom hook to use the toast context
export const useToast = () => {
  const context = useContext(ToastContext);

  if (!context) {
    throw new Error('useToast must be used within a ToastProvider');
  }

  return context;
};

export default ToastContext;
