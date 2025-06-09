import React, { useState, useEffect, useRef } from 'react';
import { Box, TextField, Button, Typography, Paper, Divider } from '@mui/material';
import axios from 'axios';

const ChatInterface = ({ projectId }) => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const chatContainerRef = useRef(null);

  useEffect(() => {
    // Scroll to the bottom on messages update
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSendMessage = async () => {
    if (input.trim()) {
      const userMessage = { sender: 'user', text: input };
      setMessages(prev => [...prev, userMessage]);
      setInput('');

      try {
        // Here you would call an AI service endpoint for chat response
        const response = await axios.post(`/api/chat/project/${projectId}`, { message: input });
        const aiMessage = { sender: 'ai', text: response.data.response };
        setMessages(prev => [...prev, aiMessage]);
      } catch (error) {
        console.error('Error in chat response:', error);
        setMessages(prev => [...prev, { sender: 'ai', text: "Sorry, I couldn't process your request." }]);
      }
    }
  };

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', height: 400 }}>
      <Box 
        ref={chatContainerRef} 
        sx={{ flexGrow: 1, overflowY: 'auto', p: 2, border: '1px solid #e0e0e0', borderRadius: 1, mb: 2 }}
      >
        {messages.length === 0 ? (
          <Typography variant="body2" color="text.secondary">Start a conversation...</Typography>
        ) : (
          messages.map((msg, index) => (
            <Box key={index} sx={{ mb: 1, textAlign: msg.sender === 'user' ? 'right' : 'left' }}>
              <Paper 
                sx={{ 
                  p: 1, 
                  display: 'inline-block', 
                  backgroundColor: msg.sender === 'user' ? '#1976d2' : '#f5f5f5',
                  color: msg.sender === 'user' ? 'white' : 'black'
                }} 
                elevation={1}
              >
                <Typography variant="body2">{msg.text}</Typography>
              </Paper>
            </Box>
          ))
        )}
      </Box>
      <Box sx={{ display: 'flex', gap: 1 }}>
        <TextField 
          value={input} 
          onChange={(e) => setInput(e.target.value)} 
          variant="outlined" 
          placeholder="Type your message..." 
          fullWidth
          onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
        />
        <Button variant="contained" onClick={handleSendMessage}>Send</Button>
      </Box>
    </Box>
  );
};

export default ChatInterface;
