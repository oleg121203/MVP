import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { useParams } from 'react-router-dom';

const AIChatInterface = () => {
  const { projectId } = useParams();
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const chatContainerRef = useRef(null);
  const API_BASE_URL = "http://localhost:8000/api/analytics";

  useEffect(() => {
    // Scroll to the bottom of the chat on new messages
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [messages]);

  useEffect(() => {
    // Fetch initial AI greeting or insights as chat starter
    const fetchInitialMessage = async () => {
      setLoading(true);
      try {
        const response = await axios.get(`${API_BASE_URL}/project/${projectId}/ai-insights`);
        const initialMessage = {
          sender: 'AI',
          text: response.data.length > 0 ? response.data[0] : "Hello! I'm ready to help with your project analytics. Ask me anything!",
          timestamp: new Date().toISOString()
        };
        setMessages([initialMessage]);
      } catch (error) {
        console.error("Error fetching initial AI message:", error);
        setMessages([{
          sender: 'AI',
          text: "Hello! I'm ready to help with your project analytics. Ask me anything!",
          timestamp: new Date().toISOString()
        }]);
      } finally {
        setLoading(false);
      }
    };
    
    fetchInitialMessage();
  }, [projectId]);

  const handleSendMessage = async () => {
    if (input.trim()) {
      const userMessage = {
        sender: 'User',
        text: input,
        timestamp: new Date().toISOString()
      };
      setMessages(prev => [...prev, userMessage]);
      setInput('');
      setLoading(true);

      try {
        // Simulate AI response - in a real scenario, this would be a POST to an AI endpoint
        const response = await axios.post(`${API_BASE_URL}/project/${projectId}/ai-chat`, { message: input });
        const aiResponse = {
          sender: 'AI',
          text: response.data.response || "I'm processing your request. Here's my response based on the project data.",
          timestamp: new Date().toISOString()
        };
        setMessages(prev => [...prev, aiResponse]);
      } catch (error) {
        console.error("Error getting AI response:", error);
        setMessages(prev => [...prev, {
          sender: 'AI',
          text: "Sorry, I couldn't process that. Please try again.",
          timestamp: new Date().toISOString()
        }]);
      } finally {
        setLoading(false);
      }
    }
  };

  return (
    <Card className="h-full flex flex-col">
      <CardHeader>
        <CardTitle>AI Chat Assistant</CardTitle>
      </CardHeader>
      <CardContent className="flex-grow overflow-hidden flex flex-col">
        <div 
          ref={chatContainerRef} 
          className="flex-grow overflow-y-auto p-4 bg-gray-50 rounded-md"
        >
          {messages.map((msg, index) => (
            <div 
              key={index} 
              className={`mb-3 ${msg.sender === 'User' ? 'text-right' : 'text-left'}`}
            >
              <span 
                className={`inline-block p-2 rounded-lg ${msg.sender === 'User' ? 'bg-blue-100 text-blue-800' : 'bg-gray-200 text-gray-800'}`}
              >
                <strong>{msg.sender}: </strong>{msg.text}
              </span>
              <div className="text-xs text-gray-500 mt-1">
                {new Date(msg.timestamp).toLocaleTimeString()}
              </div>
            </div>
          ))}
          {loading && (
            <div className="text-left mb-3">
              <span className="inline-block p-2 rounded-lg bg-gray-200 text-gray-800">
                <strong>AI: </strong>Typing...
              </span>
            </div>
          )}
        </div>
        <div className="mt-4 flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask a question about this project..."
            className="flex-grow p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={loading}
            onKeyDown={(e) => e.key === 'Enter' && handleSendMessage()}
          />
          <Button 
            onClick={handleSendMessage} 
            disabled={loading || !input.trim()}
            className="bg-blue-600 hover:bg-blue-700 text-white"
          >
            Send
          </Button>
        </div>
      </CardContent>
    </Card>
  );
};

export default AIChatInterface;
