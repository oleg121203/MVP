import React, { useEffect, useRef } from 'react';
import Button from './Button';
import './Modal.css';

/**
 * Modal component for displaying dialog windows and overlays
 *
 * @param {Object} props - Component props
 * @param {boolean} props.isOpen - Controls modal visibility
 * @param {Function} props.onClose - Function called when modal is closed
 * @param {string} [props.title] - Optional modal title
 * @param {React.ReactNode} props.children - Modal content
 * @param {React.ReactNode} [props.footer] - Optional footer content, usually action buttons
 * @param {('small'|'medium'|'large')} [props.size='medium'] - Controls modal width
 * @param {string} [props.className] - Additional CSS classes
 * @param {boolean} [props.closeOnOverlayClick=true] - Whether clicking the overlay closes the modal
 * @param {boolean} [props.closeOnEsc=true] - Whether pressing Escape closes the modal
 * @returns {JSX.Element|null} Modal component or null if closed
 */
const Modal = ({
  isOpen,
  onClose,
  title,
  children,
  footer,
  size = 'medium',
  className = '',
  closeOnOverlayClick = true,
  closeOnEsc = true,
}) => {
  const modalRef = useRef(null);
  const previousFocusRef = useRef(null);

  // Handle Escape key press
  useEffect(() => {
    const handleEscapeKey = (event) => {
      if (closeOnEsc && event.key === 'Escape') {
        onClose();
      }
    };

    if (isOpen) {
      document.addEventListener('keydown', handleEscapeKey);
    }

    return () => {
      document.removeEventListener('keydown', handleEscapeKey);
    };
  }, [isOpen, onClose, closeOnEsc]);

  // Handle focus management for accessibility
  useEffect(() => {
    if (isOpen) {
      // Store the currently focused element to restore focus later
      previousFocusRef.current = document.activeElement;

      // Focus the modal when it opens
      if (modalRef.current) {
        modalRef.current.focus();
      }
    } else {
      // Restore focus when modal closes
      if (previousFocusRef.current) {
        previousFocusRef.current.focus();
      }
    }
  }, [isOpen]);

  // Don't render anything if modal is closed
  if (!isOpen) {
    return null;
  }

  const handleOverlayClick = (event) => {
    if (closeOnOverlayClick && event.target === event.currentTarget) {
      onClose();
    }
  };

  // Determine modal width based on size prop
  const sizeClass =
    {
      small: 'modal-size-small',
      medium: 'modal-size-medium',
      large: 'modal-size-large',
    }[size] || 'modal-size-medium';

  return (
    <div
      className="modal-overlay"
      onClick={handleOverlayClick}
      role="dialog"
      aria-modal="true"
      aria-labelledby={title ? 'modal-title' : undefined}
    >
      <div
        ref={modalRef}
        className={`modal-content ${sizeClass} ${className}`.trim()}
        tabIndex={-1} // Make the modal focusable for accessibility
        onClick={(e) => e.stopPropagation()} // Prevent clicks inside modal from closing it
      >
        {title && (
          <div className="modal-header">
            <h2 id="modal-title" className="modal-title">
              {title}
            </h2>
            <button onClick={onClose} className="modal-close-button" aria-label="Close modal">
              <svg width="20" height="20" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fillRule="evenodd"
                  d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                  clipRule="evenodd"
                ></path>
              </svg>
            </button>
          </div>
        )}
        <div className="modal-body">{children}</div>
        {footer && <div className="modal-footer">{footer}</div>}
      </div>
    </div>
  );
};

/**
 * Confirmation modal with predefined structure for common confirmation dialogs
 *
 * @param {Object} props - Component props
 * @param {boolean} props.isOpen - Controls modal visibility
 * @param {Function} props.onClose - Function called when modal is closed
 * @param {string} [props.title='Confirm Action'] - Dialog title
 * @param {string|React.ReactNode} props.message - Confirmation message
 * @param {string} [props.confirmText='Confirm'] - Text for confirm button
 * @param {string} [props.cancelText='Cancel'] - Text for cancel button
 * @param {Function} props.onConfirm - Function called when action is confirmed
 * @param {('small'|'medium'|'large')} [props.size='small'] - Controls modal width
 * @param {string} [props.confirmVariant='primary'] - Button variant for confirm button
 * @returns {JSX.Element} Confirmation modal
 */
export const ConfirmationModal = ({
  isOpen,
  onClose,
  title = 'Confirm Action',
  message,
  confirmText = 'Confirm',
  cancelText = 'Cancel',
  onConfirm,
  size = 'small',
  confirmVariant = 'primary',
}) => {
  const handleConfirm = () => {
    onConfirm();
    onClose();
  };

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title={title}
      size={size}
      footer={
        <>
          <Button variant="secondary" onClick={onClose}>
            {cancelText}
          </Button>
          <Button variant={confirmVariant} onClick={handleConfirm}>
            {confirmText}
          </Button>
        </>
      }
    >
      <div className="confirmation-message">{message}</div>
    </Modal>
  );
};

export default Modal;
