// API route for chat functionality
import type { NextApiRequest, NextApiResponse } from 'next';

interface ChatRequest {
  message: string;
}

interface ChatResponse {
  reply: string;
}

interface ErrorResponse {
  message: string;
}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<ChatResponse | ErrorResponse>
) {
  if (req.method !== 'POST') {
    return res.status(405).json({ message: 'Method not allowed' });
  }

  try {
    // Connect to actual AI service via backend MCP server
    const { message } = req.body as ChatRequest;
    
    // Make request to MCP server endpoint with correct prefix
    const response = await fetch('http://localhost:8001/api/ai/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message }),
    });
    
    if (!response.ok) {
      throw new Error(`Backend responded with status ${response.status}`);
    }
    
    const data = await response.json();
    const reply = data.reply || 'No response from AI service';
    
    res.status(200).json({ reply });
  } catch (error) {
    res.status(500).json({ message: 'Internal server error' });
  }
}
