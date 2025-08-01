export const calculateSavingsRate = (income, expenses) => {
  if (income <= 0) return 0;
  return ((income - expenses) / income) * 100;
};

export const calculateEmergencyFundTarget = (monthlyExpenses, months = 6) => {
  return monthlyExpenses * months;
};

export const calculateInvestmentReturn = (initialInvestment, annualRate, years) => {
  return initialInvestment * Math.pow((1 + annualRate / 100), years);
};

export const calculateBudgetBalance = (income, expenses) => {
  return income - expenses;
};

export const categorizeExpenses = (transactions) => {
  return transactions.reduce((acc, transaction) => {
    const category = transaction.category || 'Uncategorized';
    if (!acc[category]) {
      acc[category] = 0;
    }
    acc[category] += transaction.amount;
    return acc;
  }, {});
};