import React, { useState, useEffect, useRef } from 'react';
import { v4 as uuidv4 } from 'uuid';
import { updateUserProfile, fetchUserProfile, getBotResponse } from './services/api';
import styles from './styles/FinanceAdvisor.module.css';
import BudgetCreator from './components/Budgeting/BudgetCreator';
import BudgetOverview from './components/Budgeting/BudgetOverview';
import PersonalizedBudgetAdvice from './components/Budgeting/PersonalizedBudgetAdvice';
import TransactionList from './components/Transactions/TransactionList';
import ExpenseTracker from './components/Transactions/ExpenseTracker';
import InvestmentSuggestions from './components/Investments/InvestmentSuggestions';
import InvestmentSuggestionsEnhanced from './components/Investments/InvestmentSuggestionsEnhanced';
import FinancialLessons from './components/Education/FinancialLessons';
import FinancialEducationHub from './components/Education/FinancialEducationHub';
import AIAdvisor from './components/PersonalizedAdvice/AIAdvisor';
import ProgressBar from './components/UI/ProgressBar';

const PersonalFinanceAdvisorDynamic = () => {
  const [userId] = useState(() => {
    let id = localStorage.getItem('userId');
    if (!id) {
      id = uuidv4();
      localStorage.setItem('userId', id);
    }
    return id;
  });

  const [userProfile, setUserProfile] = useState({
    age: '',
    income: 0,
    expenses: 0,
    savings: 0,
    riskTolerance: 'moderate'
  });
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [goals, setGoals] = useState([]);
  const [activeTab, setActiveTab] = useState('dashboard');
  const [userTransactions, setUserTransactions] = useState([]);
  const messagesEndRef = useRef();

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  useEffect(() => {
    async function loadUserData() {
      try {
        const profile = await fetchUserProfile(userId);
        if (profile) {
          setUserProfile(profile);
        }
      } catch (error) {
        console.error('Error loading user data:', error);
        // Use default profile if API fails
      }
    }
    loadUserData();
  }, [userId]);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = { id: uuidv4(), text: input, sender: 'user', timestamp: new Date() };
    setMessages(prev => [...prev, userMessage]);
    setInput('');

    try {
      const botResponse = await getBotResponse(userId, input, { userProfile, goals });
      const botMessage = { 
        id: uuidv4(), 
        text: botResponse.message, 
        sender: 'bot', 
        timestamp: new Date(),
        suggestions: botResponse.suggestions 
      };
      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error getting bot response:', error);
      const errorMessage = { 
        id: uuidv4(), 
        text: "Sorry, I'm having trouble responding right now. Please try again.", 
        sender: 'bot', 
        timestamp: new Date() 
      };
      setMessages(prev => [...prev, errorMessage]);
    }
  };

  const updateProfileField = async (field, value) => {
    try {
      const updatedProfile = { ...userProfile, [field]: value };
      setUserProfile(updatedProfile);
      await updateUserProfile(userId, updatedProfile);
    } catch (error) {
      console.error('Error updating profile:', error);
      // Revert the change if API call fails
      setUserProfile(userProfile);
    }
  };

  const handleExpenseUpdate = (transactions) => {
    setUserTransactions(transactions);
    // Update user profile with latest expense data
    const totalExpenses = transactions
      .filter(t => t.type === 'expense')
      .reduce((sum, t) => sum + t.amount, 0);
    const totalIncome = transactions
      .filter(t => t.type === 'income')
      .reduce((sum, t) => sum + t.amount, 0);
    
    updateProfileField('expenses', totalExpenses);
    updateProfileField('income', totalIncome);
  };

  const renderActiveTab = () => {
    switch (activeTab) {
      case 'dashboard':
        return (
          <>
            <div className={styles.chatSection}>
              <div className={styles.messagesContainer}>
                {messages.map(message => (
                  <div key={message.id} className={`${styles.message} ${styles[message.sender]}`}>
                    <div className={styles.messageText}>{message.text}</div>
                    <div className={styles.messageTime}>
                      {message.timestamp.toLocaleTimeString()}
                    </div>
                    {message.suggestions && (
                      <div className={styles.suggestions}>
                        {message.suggestions.map((suggestion, index) => (
                          <button
                            key={index}
                            className={styles.suggestionButton}
                            onClick={() => setInput(suggestion)}
                          >
                            {suggestion}
                          </button>
                        ))}
                      </div>
                    )}
                  </div>
                ))}
                <div ref={messagesEndRef} />
              </div>
              <div className={styles.inputSection}>
                <input
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                  placeholder="Ask me about your finances..."
                  className={styles.messageInput}
                />
                <button onClick={handleSend} className={styles.sendButton}>
                  Send
                </button>
              </div>
            </div>
            <div className={styles.sidebar}>
              <AIAdvisor userProfile={userProfile} />
              <ProgressBar
                label="Savings Rate"
                current={userProfile.income - userProfile.expenses}
                target={userProfile.income}
              />
            </div>
          </>
        );
      case 'budgeting':
        return (
          <div className={styles.fullWidth}>
            <PersonalizedBudgetAdvice 
              userProfile={userProfile} 
              onUpdateProfile={updateProfileField}
            />
            <BudgetCreator />
            <BudgetOverview />
          </div>
        );
      case 'expenses':
        return (
          <div className={styles.fullWidth}>
            <ExpenseTracker 
              userId={userId} 
              onExpenseUpdate={handleExpenseUpdate}
            />
            <TransactionList transactions={userTransactions} />
          </div>
        );
      case 'investments':
        return (
          <div className={styles.fullWidth}>
            <InvestmentSuggestionsEnhanced userProfile={userProfile} />
            <InvestmentSuggestions userProfile={userProfile} />
          </div>
        );
      case 'education':
        return (
          <div className={styles.fullWidth}>
            <FinancialEducationHub />
            <FinancialLessons />
          </div>
        );
      default:
        return null;
    }
  };

  return (
    <div className={styles.container}>
      <header className={styles.header}>
        <h1>🏦 Personal Finance Advisor</h1>
        <div className={styles.userInfo}>
          <span>Welcome back! Income: ${userProfile.income.toLocaleString()}</span>
          <span>Savings: ${userProfile.savings.toLocaleString()}</span>
        </div>
      </header>
      
      {/* Navigation Tabs */}
      <nav className={styles.navigation}>
        <button 
          className={`${styles.navButton} ${activeTab === 'dashboard' ? styles.active : ''}`}
          onClick={() => setActiveTab('dashboard')}
        >
          🏠 Dashboard
        </button>
        <button 
          className={`${styles.navButton} ${activeTab === 'budgeting' ? styles.active : ''}`}
          onClick={() => setActiveTab('budgeting')}
        >
          📊 Smart Budgeting
        </button>
        <button 
          className={`${styles.navButton} ${activeTab === 'expenses' ? styles.active : ''}`}
          onClick={() => setActiveTab('expenses')}
        >
          💳 Expense Tracking
        </button>
        <button 
          className={`${styles.navButton} ${activeTab === 'investments' ? styles.active : ''}`}
          onClick={() => setActiveTab('investments')}
        >
          📈 Investments
        </button>
        <button 
          className={`${styles.navButton} ${activeTab === 'education' ? styles.active : ''}`}
          onClick={() => setActiveTab('education')}
        >
          🎓 Learn Finance
        </button>
      </nav>

      <div className={styles.mainContent}>
        {renderActiveTab()}
      </div>
    </div>
  );
};

export default PersonalFinanceAdvisorDynamic;