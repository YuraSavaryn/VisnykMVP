import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import styles from './Agent.module.css';

const Agent = () => {
  const [messages, setMessages] = useState([
    { role: 'ai', content: 'Привіт! Я ШІ-журналіст «Вісник». Чим можу допомогти?' }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await axios.post('http://localhost:8000/api/v1/agent/inference', {
        session_id: 1,
        content: input
      });

      const aiMessage = { 
        role: 'ai', 
        content: typeof response.data === 'string' ? response.data : response.data.content 
      };
      
      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      setMessages(prev => [...prev, { role: 'ai', content: 'Помилка зв’язку з сервером.' }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={styles.chatWrapper}>
      <div className={styles.chatContainer}>
        <div className={styles.messagesList}>
          {messages.map((msg, index) => (
            <div key={index} className={`${styles.message} ${styles[msg.role]}`}>
              <div className={styles.bubble}>{msg.content}</div>
            </div>
          ))}
          
          {/* Анімовані крапки під час завантаження */}
          {isLoading && (
            <div className={`${styles.message} ${styles.ai}`}>
              <div className={styles.bubble}>
                <div className={styles.typingDots}>
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <form className={styles.inputArea} onSubmit={handleSendMessage}>
          <input
            type="text"
            placeholder="Запитайте щось у Вісника..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={isLoading}
          />
          <button type="submit" disabled={isLoading}>Відправити</button>
        </form>
      </div>
    </div>
  );
};

export default Agent;