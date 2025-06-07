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
    // TODO: Connect to actual AI service
    const { message } = req.body as ChatRequest;
    
    // Mock response for now
    const reply = `I received your question about: "${message}". This will connect to the AI backend soon.`;
    
    res.status(200).json({ reply });
  } catch (error) {
    res.status(500).json({ message: 'Internal server error' });
  }
}
