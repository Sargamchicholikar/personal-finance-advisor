import React, { useState } from 'react';
import styles from './styles/FinanceAdvisor.module.css';
import PersonalizedBudgetAdvice from './components/Budgeting/PersonalizedBudgetAdvice';
import ExpenseTracker from './components/Transactions/ExpenseTracker';
import InvestmentSuggestionsEnhanced from './components/Investments/InvestmentSuggestionsEnhanced';
import FinancialEducationHub from './components/Education/FinancialEducationHub';

const PersonalFinanceAdvisorSimple = () => {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [userProfile] = useState({
    income: 5000,
    savings: 1500,
    expenses: 3000
  });

  const renderActiveTab = () => {
    switch (activeTab) {
      case 'dashboard':
        return (
          <div className={styles.chatContainer}>
            <h2>🏠 Financial Dashboard</h2>
            <div style={{ 
              padding: '2rem', 
              backgroundColor: 'white', 
              borderRadius: '12px',
              boxShadow: '0 4px 12px rgba(0,0,0,0.1)'
            }}>
              <h3>Welcome to Your Personal Finance Advisor!</h3>
              <p>Your financial overview:</p>
              <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(3, 1fr)',
                gap: '1rem',
                marginTop: '1rem'
              }}>
                <div style={{
                  padding: '1rem',
                  backgroundColor: '#e8f5e8',
                  borderRadius: '8px',
                  textAlign: 'center'
                }}>
                  <h4 style={{ color: '#28a745', margin: '0 0 0.5rem 0' }}>Income</h4>
                  <p style={{ fontSize: '1.5rem', fontWeight: 'bold', margin: 0 }}>
                    ${userProfile.income.toLocaleString()}
                  </p>
                </div>
                <div style={{
                  padding: '1rem',
                  backgroundColor: '#fff3cd',
                  borderRadius: '8px',
                  textAlign: 'center'
                }}>
                  <h4 style={{ color: '#856404', margin: '0 0 0.5rem 0' }}>Expenses</h4>
                  <p style={{ fontSize: '1.5rem', fontWeight: 'bold', margin: 0 }}>
                    ${userProfile.expenses.toLocaleString()}
                  </p>
                </div>
                <div style={{
                  padding: '1rem',
                  backgroundColor: '#d1ecf1',
                  borderRadius: '8px',
                  textAlign: 'center'
                }}>
                  <h4 style={{ color: '#0c5460', margin: '0 0 0.5rem 0' }}>Savings</h4>
                  <p style={{ fontSize: '1.5rem', fontWeight: 'bold', margin: 0 }}>
                    ${userProfile.savings.toLocaleString()}
                  </p>
                </div>
              </div>
            </div>
          </div>
        );
      case 'budgeting':
        return (
          <div className={styles.chatContainer}>
            <PersonalizedBudgetAdvice userProfile={userProfile} />
          </div>
        );
      case 'expenses':
        return (
          <div className={styles.chatContainer}>
            <ExpenseTracker />
          </div>
        );
      case 'investments':
        return (
          <div className={styles.chatContainer}>
            <InvestmentSuggestionsEnhanced userProfile={userProfile} />
          </div>
        );
      case 'education':
        return (
          <div className={styles.chatContainer}>
            <FinancialEducationHub />
          </div>
        );
      default:
        return (
          <div className={styles.chatContainer}>
            <h2>Coming Soon</h2>
            <p>This feature is under development.</p>
          </div>
        );
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

export default PersonalFinanceAdvisorSimple;
