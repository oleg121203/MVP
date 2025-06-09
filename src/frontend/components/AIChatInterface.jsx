import React, { useState } from 'react';
import io from 'socket.io-client';

const AIChatInterface = ({ projectId }) => {
  const [messages, setMessages] = useState([
    { sender: 'AI', text: 'Hello! How can I help with your project analysis?' }
  ]);
  const [inputText, setInputText] = useState('');
  
  const handleSend = () => {
    if (!inputText.trim()) return;
    
    // Add user message
    const userMessage = { sender: 'user', text: inputText };
    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    
    // Simulate AI response
    setTimeout(() => {
      setMessages(prev => [...prev, {
        sender: 'AI', 
        text: `Based on project ${projectId}, I recommend reviewing the budget utilization metrics.`
      }]);
    }, 1000);
  };

  return (
    <div className="ai-chat">
      <div className="chat-messages">
        {messages.map((msg, i) => (
          <div key={i} className={`message ${msg.sender}`}>
            <strong>{msg.sender}:</strong> {msg.text}
          </div>
        ))}
      </div>
      <div className="chat-input">
        <input 
          type="text" 
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSend()}
          placeholder="Ask about project analytics..."
        />
        <button onClick={handleSend}>Send</button>
      </div>
    </div>
  );
};

export default AIChatInterface;
