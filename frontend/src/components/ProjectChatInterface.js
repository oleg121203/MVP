import React, { useState, useEffect, useRef } from 'react';
import { postProjectChatMessage } from '../services/apiService';
import { useTheme } from '../context/ThemeContext';
import { useLocalization } from '../context/LocalizationContext';
import { useToast } from '../context/ToastContext';
import { Button } from './ui';
import { FaPaperPlane, FaUser, FaRobot } from 'react-icons/fa';

const ProjectChatInterface = ({ projectId }) => {
  const { theme } = useTheme();
  const { t } = useLocalization();
  const { success, error, info } = useToast();
  const [messages, setMessages] = useState([
    {
      sender: 'ai',
      text: t("Hello! I'm your AI assistant for this project. How can I help?"),
      timestamp: new Date().toISOString(),
    },
  ]);
  const [currentInput, setCurrentInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const [typingTimeout, setTypingTimeout] = useState(null);

  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSendMessage = async () => {
    const userInputText = currentInput.trim();
    if (!userInputText || isLoading) return;

    const currentTime = new Date().toISOString();
    const newUserMessage = {
      sender: 'user',
      text: userInputText,
      timestamp: currentTime,
    };

    setMessages((prevMessages) => [...prevMessages, newUserMessage]);
    setCurrentInput('');
    setIsLoading(true);

    // Show typing indicator with random typing duration
    setIsTyping(true);

    // Clear any existing typing timeout
    if (typingTimeout) {
      clearTimeout(typingTimeout);
    }

    try {
      // Send message to API
      const data = await postProjectChatMessage(projectId, userInputText, messages);

      // Calculate a realistic typing delay based on response length (50-150ms per character with some randomness)
      const baseDelay = 500; // minimum delay
      const charDelay = Math.min(data.response.length * (50 + Math.random() * 100), 5000); // cap at 5 seconds
      const typingDelay = baseDelay + charDelay;

      // Set timeout for typing effect
      const timeout = setTimeout(() => {
        const aiResponse = {
          sender: 'ai',
          text: data.response,
          timestamp: new Date().toISOString(),
        };

        setMessages((prevMessages) => [...prevMessages, aiResponse]);
        setIsTyping(false);
      }, typingDelay);

      setTypingTimeout(timeout);
    } catch (err) {
      console.error('Chat error:', err);
      const errorMessage = {
        sender: 'ai',
        text: `${t('Error')}: ${err.message || t('Failed to get response')}`,
        timestamp: new Date().toISOString(),
        isError: true,
      };

      setMessages((prevMessages) => [...prevMessages, errorMessage]);
      setIsTyping(false);
      error(t('Failed to send message. Please try again.'));
    } finally {
      setIsLoading(false);
      // Focus back on input after sending
      inputRef.current?.focus();
    }
  };

  // Clean up typing timeout on unmount
  useEffect(() => {
    return () => {
      if (typingTimeout) {
        clearTimeout(typingTimeout);
      }
    };
  }, [typingTimeout]);

  const handleKeyPress = (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      handleSendMessage();
    }
  };

  // Format timestamp to a readable format
  const formatTimestamp = (timestamp) => {
    const date = new Date(timestamp);
    const now = new Date();
    const isToday =
      date.getDate() === now.getDate() &&
      date.getMonth() === now.getMonth() &&
      date.getFullYear() === now.getFullYear();

    if (isToday) {
      return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    } else {
      return (
        date.toLocaleDateString([], { month: 'short', day: 'numeric' }) +
        ' ' +
        date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      );
    }
  };

  return (
    <div
      className={`border border-gray-200 dark:border-gray-700 rounded-lg bg-white dark:bg-gray-800 p-6 mt-8 flex flex-col shadow-md transition-all h-[600px]`}
    >
      <h4 className="text-xl font-semibold text-gray-800 dark:text-gray-100 mb-5 pb-3 border-b border-gray-200 dark:border-gray-700 text-center">
        {t('Project Chat')}
      </h4>
      <div className="flex-1 overflow-y-auto p-4 bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg mb-5 shadow-inner">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`flex mb-4 animate-fadeIn ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div className={`flex flex-col max-w-[80%]`}>
              <div
                className={`flex items-start ${msg.sender === 'user' ? 'flex-row-reverse' : 'flex-row'}`}
              >
                {msg.sender === 'user' && (
                  <span className="flex items-center justify-center w-8 h-8 rounded-full bg-blue-100 dark:bg-blue-900 text-blue-600 dark:text-blue-300 ml-2">
                    <FaUser className="text-sm" />
                  </span>
                )}
                {msg.sender === 'ai' && (
                  <span className="flex items-center justify-center w-8 h-8 rounded-full bg-purple-100 dark:bg-purple-900 text-purple-600 dark:text-purple-300 mr-2">
                    <FaRobot className="text-sm" />
                  </span>
                )}
                <div
                  className={`p-3 rounded-lg shadow-sm ${
                    msg.isError
                      ? 'bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-200'
                      : msg.sender === 'user'
                        ? 'bg-blue-500 text-white'
                        : 'bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-200'
                  }`}
                >
                  {msg.text}
                </div>
              </div>
              {msg.timestamp && (
                <div
                  className={`text-xs text-gray-500 dark:text-gray-400 mt-1 ${msg.sender === 'user' ? 'text-right' : 'text-left'}`}
                >
                  {formatTimestamp(msg.timestamp)}
                </div>
              )}
            </div>
          </div>
        ))}

        {isTyping && (
          <div className="flex mb-4 justify-start">
            <div className="flex flex-col max-w-[80%]">
              <div className="flex items-start">
                <span className="flex items-center justify-center w-8 h-8 rounded-full bg-purple-100 dark:bg-purple-900 text-purple-600 dark:text-purple-300 mr-2">
                  <FaRobot className="text-sm" />
                </span>
                <div className="p-3 rounded-lg bg-gray-200 dark:bg-gray-700 flex items-center">
                  <div className="flex space-x-1">
                    <div
                      className="w-2 h-2 rounded-full bg-gray-400 dark:bg-gray-500 animate-bounce"
                      style={{ animationDelay: '0ms' }}
                    ></div>
                    <div
                      className="w-2 h-2 rounded-full bg-gray-400 dark:bg-gray-500 animate-bounce"
                      style={{ animationDelay: '150ms' }}
                    ></div>
                    <div
                      className="w-2 h-2 rounded-full bg-gray-400 dark:bg-gray-500 animate-bounce"
                      style={{ animationDelay: '300ms' }}
                    ></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <div className="mt-auto">
        <div className="flex items-center gap-2">
          <textarea
            ref={inputRef}
            value={currentInput}
            onChange={(e) => setCurrentInput(e.target.value)}
            onKeyDown={handleKeyPress}
            placeholder={t('Type your message...')}
            disabled={isLoading}
            className="flex-1 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-200 resize-none h-[60px]"
            rows="2"
          />
          <Button
            onClick={handleSendMessage}
            disabled={isLoading || !currentInput.trim()}
            variant="primary"
            className="h-[60px] px-4 flex items-center gap-2 whitespace-nowrap"
            aria-label={t('Send message')}
          >
            {isLoading ? (
              t('Sending...')
            ) : (
              <>
                <FaPaperPlane className="text-sm" />
                <span>{t('Send')}</span>
              </>
            )}
          </Button>
        </div>
      </div>
    </div>
  );
};

export default ProjectChatInterface;
