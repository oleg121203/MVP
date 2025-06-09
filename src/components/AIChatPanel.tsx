import React from 'react';
import styles from './AIChatPanel.module.css';
import { FixedSizeList as List } from 'react-window';

type AIChatPanelProps = {
  projectId: string;
  onSendQuery: (query: string) => Promise<string>;
};

export const AIChatPanel: React.FC<AIChatPanelProps> = ({ projectId, onSendQuery }) => {
  const [messages, setMessages] = React.useState<Array<{sender: string, text: string}>>([]);
  const [inputValue, setInputValue] = React.useState('');

  const handleSend = async () => {
    if (!inputValue.trim()) return;
    
    const userMessage = { sender: 'user', text: inputValue };
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    
    try {
      const aiResponse = await onSendQuery(inputValue);
      setMessages(prev => [...prev, { sender: 'ai', text: aiResponse }]);
    } catch (error) {
      setMessages(prev => [...prev, { sender: 'ai', text: 'Error processing query' }]);
    }
  };

  const MessageRow = ({ index, style, data }) => (
    <div style={style} className={styles[data[index].sender]}>
      {data[index].text}
    </div>
  );

  return (
    <div className={styles.chatContainer}>
      <div className={styles.messages}>
        <List
          height={200}
          itemCount={messages.length}
          itemSize={50}
          width="100%"
          itemData={messages}
        >
          {MessageRow}
        </List>
      </div>
      <div className={styles.inputArea}>
        <input 
          type="text" 
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSend()}
        />
        <button onClick={handleSend}>Send</button>
      </div>
    </div>
  );
};
