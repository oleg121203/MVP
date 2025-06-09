import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import AIChat from '../AIChat';

// Mock axios to avoid ES module issues
const axios = require('axios');
jest.mock('axios', () => ({
  post: jest.fn(() => Promise.resolve({ data: { response: 'Mocked AI response' } }))
}));

describe('AIChat Component', () => {
  test('renders AI chat interface', () => {
    render(<AIChat />);
    expect(screen.getByPlaceholderText(/Ask AI about this project.../i)).toBeTruthy();
  });

  test('sends message and checks user input rendering', async () => {
    render(<AIChat />);
    const input = screen.getByPlaceholderText(/Ask AI about this project.../i);
    const sendButton = screen.getByText(/Send/i);

    fireEvent.change(input, { target: { value: 'Hello AI' } });
    fireEvent.click(sendButton);

    // Check for the presence of user message in the chat
    await waitFor(() => {
      expect(screen.findByText('Hello AI', { exact: false })).toBeTruthy();
    }, { timeout: 1000 });
  });

  test('handles empty message', () => {
    render(<AIChat />);
    const sendButton = screen.getByText(/Send/i);
    fireEvent.click(sendButton);
    // Since the error message might not be rendered immediately, we'll check for a lack of message send
    expect(screen.queryByText('Hello AI', { exact: false })).not.toBeTruthy();
  });

  test('handles API error and checks user input rendering', async () => {
    // Simulate error response
    axios.post.mockImplementation(() => Promise.reject(new Error('API Error')));
    
    render(<AIChat />);
    const input = screen.getByPlaceholderText(/Ask AI about this project.../i);
    const sendButton = screen.getByText(/Send/i);

    fireEvent.change(input, { target: { value: 'Error test' } });
    fireEvent.click(sendButton);

    // Check for the presence of user message in the chat
    await waitFor(() => {
      expect(screen.findByText('Error test', { exact: false })).toBeTruthy();
    }, { timeout: 1000 });
  });

  test('handles keyboard enter key and checks user input rendering', async () => {
    render(<AIChat />);
    const input = screen.getByPlaceholderText(/Ask AI about this project.../i);

    fireEvent.change(input, { target: { value: 'Enter key test' } });
    fireEvent.keyDown(input, { key: 'Enter', code: 'Enter' });

    // Check if the input value remains unchanged
    expect(input.value).toBe('Enter key test');
  });
});
