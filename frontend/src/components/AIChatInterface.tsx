import { useState } from 'react';
import { 
  Box, 
  Input, 
  Button, 
  Text, 
  VStack,
  Flex,
  useToast as useChakraToast
} from '@chakra-ui/react';

export default function AIChatInterface() {
  const [messages, setMessages] = useState<Array<{role: string, content: string}>>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const toast = useChakraToast();

  const handleSend = async () => {
    if (!input.trim()) return;
    
    const userMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);
    
    try {
      const response = await fetch('http://localhost:8000/api/ai/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: input })
      });
      
      const data = await response.json();
      setMessages(prev => [...prev, 
        { role: 'ai', content: data.reply },
        ...(data.suggestions?.map((s: string) => ({ role: 'ai', content: s })) || [])
      ]);
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to get AI response',
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <VStack gap={4} align="stretch">
      <Box 
        borderWidth="1px" 
        borderRadius="md" 
        p={4} 
        h="400px" 
        overflowY="auto"
      >
        {messages.map((msg, i) => (
          <Text key={i} mb={2} color={msg.role === 'user' ? 'blue.500' : 'green.500'}>
            <strong>{msg.role === 'user' ? 'You:' : 'AI:'}</strong> {msg.content}
          </Text>
        ))}
      </Box>
      
      <Flex gap={2}>
        <Input 
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask about HVAC design..."
          onKeyPress={(e) => e.key === 'Enter' && handleSend()}
        />
        <Button 
          colorScheme="blue" 
          onClick={handleSend}
          isLoading={isLoading}
          loadingText="Sending"
        >
          Send
        </Button>
      </Flex>
    </VStack>
  );
}
