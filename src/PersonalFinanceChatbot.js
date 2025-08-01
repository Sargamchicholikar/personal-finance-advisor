import React, { useState, useEffect, useRef } from 'react';
import { v4 as uuidv4 } from 'uuid';
import { getBotResponse } from './services/api';
import styles from './styles/FinanceAdvisor.module.css';

const PersonalFinanceChatbot = () => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [userProfile, setUserProfile] = useState({
    income: null,
    expenses: null,
    savings: null,
    debt: null,
    goals: [],
    conversationContext: {}
  });
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => {
    // Load saved profile
    const savedProfile = localStorage.getItem('userFinanceProfile');
    if (savedProfile) {
      setUserProfile(JSON.parse(savedProfile));
    }

    // Add welcome message
    const welcomeMessage = {
      id: uuidv4(),
      text: "🌟 **Welcome to Your Professional Finance Advisor**\n\nI'm your AI-powered financial consultant, ready to provide expert guidance tailored to your unique situation. My capabilities include:\n\n💼 **Strategic Budget Planning** - Comprehensive income allocation\n📈 **Advanced Analytics** - Deep spending pattern analysis  \n🎯 **Debt Optimization** - Scientifically-backed payoff strategies\n💎 **Investment Intelligence** - Risk-assessed portfolio recommendations\n🏆 **Goal Achievement** - Milestone-driven financial planning\n📚 **Financial Education** - Expert insights and market trends\n\n**Ready to transform your financial future?** Share your income, expenses, or specific goals - I'll provide personalized, actionable strategies to help you succeed.",
      sender: 'bot',
      timestamp: new Date().toLocaleTimeString()
    };
    setMessages([welcomeMessage]);
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const saveUserProfile = (profile) => {
    setUserProfile(profile);
    localStorage.setItem('userFinanceProfile', JSON.stringify(profile));
  };

  const handleSend = async () => {
    if (!inputMessage.trim()) return;

    const userMessage = {
      id: uuidv4(),
      text: inputMessage,
      sender: 'user',
      timestamp: new Date().toLocaleTimeString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      // Get bot response with conversation context
      const conversationHistory = [...messages, userMessage];
      const botResponseText = await getBotResponse(inputMessage, userProfile, conversationHistory);
      
      // Process and update user profile based on message
      const updatedProfile = processUserMessage(inputMessage, userProfile);
      if (JSON.stringify(updatedProfile) !== JSON.stringify(userProfile)) {
        saveUserProfile(updatedProfile);
      }

      const botMessage = {
        id: uuidv4(),
        text: botResponseText,
        sender: 'bot',
        timestamp: new Date().toLocaleTimeString()
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error getting bot response:', error);
      const errorMessage = {
        id: uuidv4(),
        text: "I'm having trouble right now. Could you try rephrasing your question?",
        sender: 'bot',
        timestamp: new Date().toLocaleTimeString()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const processUserMessage = (message, profile) => {
    const lowerMessage = message.toLowerCase();
    let updatedProfile = { ...profile };

    // Enhanced income extraction with annual conversion
    const numbers = message.match(/\d+/g);
    const amount = numbers ? parseFloat(numbers[0]) : null;
    
    if (amount && (lowerMessage.includes('make') || lowerMessage.includes('earn') || lowerMessage.includes('income') || lowerMessage.includes('salary') || lowerMessage.includes('update'))) {
      // Check if it's annual and convert to monthly
      const isAnnual = lowerMessage.includes('annual') || lowerMessage.includes('yearly') || lowerMessage.includes('year') || lowerMessage.includes('per year');
      const monthlyIncome = isAnnual ? Math.round(amount / 12) : amount;
      
      if (monthlyIncome > 0 && monthlyIncome < 1000000) {
        updatedProfile.income = monthlyIncome;
        updatedProfile.lastUpdated = new Date().toISOString();
      }
    }

    // Enhanced expense extraction
    if (amount && (lowerMessage.includes('spend') || lowerMessage.includes('cost') || lowerMessage.includes('expense'))) {
      if (lowerMessage.includes('rent') || lowerMessage.includes('housing')) {
        updatedProfile.rentExpense = amount;
      } else {
        updatedProfile.expenses = amount;
      }
    }

    // Enhanced savings extraction  
    if (amount && (lowerMessage.includes('saved') || lowerMessage.includes('saving') || lowerMessage.includes('emergency fund'))) {
      updatedProfile.savings = amount;
    }

    // Enhanced debt extraction
    if (amount && (lowerMessage.includes('debt') || lowerMessage.includes('owe') || lowerMessage.includes('credit card'))) {
      updatedProfile.debt = amount;
    }

    // Track conversation context
    if (!updatedProfile.conversationContext) {
      updatedProfile.conversationContext = {};
    }
    if (lowerMessage.includes('budget')) updatedProfile.conversationContext.discussedBudget = true;
    if (lowerMessage.includes('invest')) updatedProfile.conversationContext.discussedInvestment = true;
    if (lowerMessage.includes('debt')) updatedProfile.conversationContext.discussedDebt = true;
    if (lowerMessage.includes('save')) updatedProfile.conversationContext.discussedSaving = true;

    return updatedProfile;
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const quickActions = [
    "I make $5000 per month",
    "Update my income to $75000 annually", 
    "Help me create a budget",
    "I have $2000 in credit card debt",
    "How should I start investing?",
    "I want to save for a house"
  ];

  const handleQuickAction = (action) => {
    setInputMessage(action);
    // Small delay to ensure the input is set before focusing
    setTimeout(() => {
      inputRef.current?.focus();
    }, 10);
  };

  return (
    <div className={styles.chatbotContainer}>
      <div className={styles.chatHeader}>
        <div className={styles.botAvatar}>💰</div>
        <div className={styles.botInfo}>
          <h3>Professional Finance Advisor</h3>
          <div className={styles.onlineStatus}>AI-Powered Financial Guidance</div>
        </div>
        {userProfile.income && (
          <div className={styles.profileSummary}>
            <div><strong>Monthly Income:</strong> ${userProfile.income?.toLocaleString()}</div>
            {userProfile.expenses && <div><strong>Expenses:</strong> ${userProfile.expenses?.toLocaleString()}</div>}
            {userProfile.savings && <div><strong>Savings:</strong> ${userProfile.savings?.toLocaleString()}</div>}
            {userProfile.debt && <div><strong>Debt:</strong> ${userProfile.debt?.toLocaleString()}</div>}
          </div>
        )}
      </div>

      <div className={styles.messagesContainer}>
        {messages.map((message) => (
          <div key={message.id} className={`${styles.messageWrapper} ${message.sender === 'user' ? styles.userMessage : styles.botMessage}`}>
            <div className={styles.messageContent}>
              <div className={styles.messageText}>
                {message.text.split('\n').map((line, index) => (
                  <div key={index}>
                    {line.split('**').map((part, partIndex) => 
                      partIndex % 2 === 0 ? part : <strong key={partIndex}>{part}</strong>
                    )}
                  </div>
                ))}
              </div>
              <div className={styles.messageTime}>{message.timestamp}</div>
            </div>
          </div>
        ))}

        {isLoading && (
          <div className={`${styles.messageWrapper} ${styles.botMessage}`}>
            <div className={styles.messageContent}>
              <div className={styles.typingIndicator}>
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {messages.length === 1 && (
        <div className={styles.quickActions}>
          <p>Try asking about:</p>
          <div className={styles.quickActionButtons}>
            {quickActions.map((action, index) => (
              <button
                key={index}
                className={styles.quickActionButton}
                onClick={() => handleQuickAction(action)}
              >
                {action}
              </button>
            ))}
          </div>
        </div>
      )}

      <div className={styles.inputContainer}>
        <textarea
          ref={inputRef}
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Ask me anything about your finances... (e.g., 'I earn $75000 annually' or 'Update my income to $80000')"
          className={styles.messageInput}
          rows={1}
          disabled={isLoading}
        />
        <button
          onClick={handleSend}
          disabled={!inputMessage.trim() || isLoading}
          className={styles.sendButton}
        >
          {isLoading ? '...' : '→'}
        </button>
      </div>
    </div>
  );
};

export default PersonalFinanceChatbot;
