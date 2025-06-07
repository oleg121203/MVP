import React, { Component, ErrorInfo, ReactNode } from 'react';

interface ErrorBoundaryProps {
  children: ReactNode;
}

interface ErrorBoundaryState {
  hasError: boolean;
}

export class ErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(_: Error): ErrorBoundaryState {
    return { hasError: true };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('ErrorBoundary caught an error:', error, errorInfo);

    // In a real app, you would send this to an error tracking service
    if (process.env.NODE_ENV === 'production') {
      // Error tracking service integration would go here
    }
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="p-4 bg-red-50 text-red-600 border border-red-200 rounded">
          <h2 className="font-bold">Something went wrong.</h2>
          <p>Our team has been notified. Please try again later.</p>
        </div>
      );
    }

    return this.props.children;
  }
}
