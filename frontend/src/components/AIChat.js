import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './AIChat.css';

const API_URL = 'http://localhost:8001/api/analytics';

const AIChat = ({ projectId }) => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const chatContainerRef = useRef(null);

  useEffect(() => {
    // Scroll to the bottom of the chat on new messages
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [messages]);

  const sendMessage = async () => {
    if (input.trim()) {
      const userMessage = { sender: 'user', text: input };
      setMessages([...messages, userMessage]);
      setInput('');

      try {
        const response = await axios.post(`${API_URL}/chat/${projectId}`, { message: input });
        const aiResponse = { sender: 'ai', text: response.data.response };
        setMessages((prevMessages) => [...prevMessages, aiResponse]);
      } catch (error) {
        console.error('Error sending message to AI:', error);
        setMessages((prevMessages) => [...prevMessages, { sender: 'ai', text: 'Error communicating with AI. Please try again.' }]);
      }
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      sendMessage();
    }
  };

  return (
    <div className="ai-chat-container">
      <div className="chat-messages" ref={chatContainerRef}>
        {messages.map((msg, index) => (
          <div key={index} className={`chat-message ${msg.sender === 'user' ? 'user-message' : 'ai-message'}`}>
            <strong>{msg.sender === 'user' ? 'You' : 'AI'}</strong>: {msg.text}
          </div>
        ))}
      </div>
      <div className="chat-input">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Ask AI about this project..."
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
};

export default AIChat;
