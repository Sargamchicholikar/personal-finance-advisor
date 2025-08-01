import React, { useState, useEffect } from 'react';
import { getBudgetData } from '../../services/budgetService';
import { getPersonalizedAdvice } from '../../services/api';
import styles from '../../styles/Budgeting.module.css';

const PersonalizedBudgetAdvice = ({ userProfile, onUpdateProfile }) => {
  const [budgetAdvice, setBudgetAdvice] = useState('');
  const [budgetGoals, setBudgetGoals] = useState([]);
  const [monthlyBudget, setMonthlyBudget] = useState({
    housing: 0,
    food: 0,
    transportation: 0,
    entertainment: 0,
    savings: 0,
    emergency: 0
  });
  const [customGoal, setCustomGoal] = useState({ name: '', amount: '', deadline: '' });

  useEffect(() => {
    generatePersonalizedBudget();
  }, [userProfile]);

  const generatePersonalizedBudget = async () => {
    try {
      const advice = await getPersonalizedAdvice({
        ...userProfile,
        requestType: 'budget_planning'
      });
      
      setBudgetAdvice(advice.advice);
      
      // Generate recommended budget allocation based on 50/30/20 rule
      const netIncome = userProfile.income - (userProfile.income * 0.2); // After taxes
      setMonthlyBudget({
        housing: Math.round(netIncome * 0.30),
        food: Math.round(netIncome * 0.15),
        transportation: Math.round(netIncome * 0.15),
        entertainment: Math.round(netIncome * 0.10),
        savings: Math.round(netIncome * 0.20),
        emergency: Math.round(netIncome * 0.10)
      });
    } catch (error) {
      console.error('Error generating personalized budget:', error);
    }
  };

  const addCustomGoal = () => {
    if (customGoal.name && customGoal.amount && customGoal.deadline) {
      const newGoal = {
        id: Date.now(),
        name: customGoal.name,
        targetAmount: parseFloat(customGoal.amount),
        currentAmount: 0,
        deadline: customGoal.deadline,
        category: 'custom',
        progress: 0
      };
      
      setBudgetGoals([...budgetGoals, newGoal]);
      setCustomGoal({ name: '', amount: '', deadline: '' });
    }
  };

  const updateGoalProgress = (goalId, amount) => {
    setBudgetGoals(goals => goals.map(goal => {
      if (goal.id === goalId) {
        const newCurrentAmount = goal.currentAmount + parseFloat(amount);
        return {
          ...goal,
          currentAmount: newCurrentAmount,
          progress: Math.min((newCurrentAmount / goal.targetAmount) * 100, 100)
        };
      }
      return goal;
    }));
  };

  return (
    <div className={styles.personalizedBudgetContainer}>
      <h3 className={styles.sectionTitle}>🎯 Personalized Budget Plan</h3>
      
      {/* Budget Advice */}
      <div className={styles.adviceSection}>
        <h4>Your Personalized Advice</h4>
        <p className={styles.adviceText}>{budgetAdvice}</p>
      </div>

      {/* Recommended Budget Allocation */}
      <div className={styles.budgetAllocation}>
        <h4>Recommended Monthly Allocation</h4>
        <div className={styles.allocationGrid}>
          {Object.entries(monthlyBudget).map(([category, amount]) => (
            <div key={category} className={styles.allocationCard}>
              <span className={styles.categoryName}>
                {category.charAt(0).toUpperCase() + category.slice(1)}
              </span>
              <span className={styles.categoryAmount}>${amount}</span>
              <div className={styles.categoryPercentage}>
                {((amount / userProfile.income) * 100).toFixed(1)}%
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Financial Goals */}
      <div className={styles.goalsSection}>
        <h4>Your Financial Goals</h4>
        
        {/* Add Custom Goal */}
        <div className={styles.addGoalForm}>
          <input
            type="text"
            placeholder="Goal name (e.g., Emergency Fund)"
            value={customGoal.name}
            onChange={(e) => setCustomGoal({...customGoal, name: e.target.value})}
            className={styles.goalInput}
          />
          <input
            type="number"
            placeholder="Target amount"
            value={customGoal.amount}
            onChange={(e) => setCustomGoal({...customGoal, amount: e.target.value})}
            className={styles.goalInput}
          />
          <input
            type="date"
            value={customGoal.deadline}
            onChange={(e) => setCustomGoal({...customGoal, deadline: e.target.value})}
            className={styles.goalInput}
          />
          <button onClick={addCustomGoal} className={styles.addGoalButton}>
            Add Goal
          </button>
        </div>

        {/* Goals List */}
        <div className={styles.goalsList}>
          {budgetGoals.map(goal => (
            <div key={goal.id} className={styles.goalCard}>
              <div className={styles.goalHeader}>
                <h5>{goal.name}</h5>
                <span className={styles.goalProgress}>{goal.progress.toFixed(1)}%</span>
              </div>
              <div className={styles.goalProgressBar}>
                <div 
                  className={styles.goalProgressFill}
                  style={{ width: `${goal.progress}%` }}
                />
              </div>
              <div className={styles.goalDetails}>
                <span>${goal.currentAmount} / ${goal.targetAmount}</span>
                <span>Due: {new Date(goal.deadline).toLocaleDateString()}</span>
              </div>
              <div className={styles.goalActions}>
                <input
                  type="number"
                  placeholder="Add amount"
                  className={styles.progressInput}
                  onKeyPress={(e) => {
                    if (e.key === 'Enter') {
                      updateGoalProgress(goal.id, e.target.value);
                      e.target.value = '';
                    }
                  }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default PersonalizedBudgetAdvice;
