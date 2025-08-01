import { v4 as uuidv4 } from 'uuid';

// Function to create a new budget
export const createBudget = (userId, budgetData) => {
  const budget = {
    id: uuidv4(),
    ...budgetData,
    createdAt: new Date().toISOString(),
  };

  // Save budget to localStorage as a fallback
  const existingBudgets = JSON.parse(localStorage.getItem(`budgets_${userId}`) || '[]');
  existingBudgets.push(budget);
  localStorage.setItem(`budgets_${userId}`, JSON.stringify(existingBudgets));

  return budget;
};

// Function to update an existing budget
export const updateBudget = (userId, budgetId, updatedData) => {
  const existingBudgets = JSON.parse(localStorage.getItem(`budgets_${userId}`) || '[]');
  const budgetIndex = existingBudgets.findIndex(b => b.id === budgetId);

  if (budgetIndex !== -1) {
    existingBudgets[budgetIndex] = {
      ...existingBudgets[budgetIndex],
      ...updatedData,
    };
    localStorage.setItem(`budgets_${userId}`, JSON.stringify(existingBudgets));
    return existingBudgets[budgetIndex];
  }

  throw new Error('Budget not found');
};

// Function to retrieve all budgets for a user
export const getBudgets = (userId) => {
  return JSON.parse(localStorage.getItem(`budgets_${userId}`) || '[]');
};

// Function to delete a budget
export const deleteBudget = (userId, budgetId) => {
  const existingBudgets = JSON.parse(localStorage.getItem(`budgets_${userId}`) || '[]');
  const updatedBudgets = existingBudgets.filter(b => b.id !== budgetId);
  localStorage.setItem(`budgets_${userId}`, JSON.stringify(updatedBudgets));
  return updatedBudgets;
};

// Function to get budget data
export const getBudgetData = (userId) => {
  try {
    const budgets = JSON.parse(localStorage.getItem(`budgets_${userId}`) || '[]');
    
    // If no budgets exist, return default data
    if (budgets.length === 0) {
      return {
        totalIncome: 0,
        totalExpenses: 0,
        remainingBalance: 0,
        categories: [],
        budgets: []
      };
    }

    // Calculate total income and expenses from all budgets
    const totalIncome = budgets.reduce((sum, budget) => sum + (budget.income || 0), 0);
    const totalExpenses = budgets.reduce((sum, budget) => sum + (budget.expenses || 0), 0);
    
    return {
      totalIncome,
      totalExpenses,
      remainingBalance: totalIncome - totalExpenses,
      categories: budgets.map(b => b.category).filter(Boolean),
      budgets
    };
  } catch (error) {
    console.error('Error getting budget data:', error);
    return {
      totalIncome: 0,
      totalExpenses: 0,
      remainingBalance: 0,
      categories: [],
      budgets: []
    };
  }
};