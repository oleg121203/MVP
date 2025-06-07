import React from 'react';
import './Card.css';

/**
 * Card component for displaying content in a contained, styled box
 *
 * @param {Object} props - Component props
 * @param {React.ReactNode} props.children - Content to display inside the card
 * @param {string} [props.title] - Optional card title
 * @param {React.ReactNode} [props.footer] - Optional footer content (buttons, info, etc.)
 * @param {string} [props.className] - Additional CSS classes
 * @param {('outlined'|'elevated'|'plain')} [props.variant='elevated'] - Card style variant
 * @param {Function} [props.onClick] - Optional click handler for the entire card
 * @returns {JSX.Element} Card component
 */
const Card = ({ children, title, footer, className = '', variant = 'elevated', onClick }) => {
  // Determine variant class
  const variantClass = `card-${variant}`;

  // Handle click if provided
  const handleClick = () => {
    if (onClick) onClick();
  };

  // Add pointer cursor style if card is clickable
  const clickableClass = onClick ? 'card-clickable' : '';

  return (
    <div className={`card ${variantClass} ${clickableClass} ${className}`} onClick={handleClick}>
      {title && <div className="card-header">{title}</div>}
      <div className="card-body">{children}</div>
      {footer && <div className="card-footer">{footer}</div>}
    </div>
  );
};

export default Card;
