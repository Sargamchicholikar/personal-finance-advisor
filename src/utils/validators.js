export const validateIncome = (income) => {
  if (typeof income !== 'number' || income < 0) {
    return 'Income must be a non-negative number.';
  }
  return null;
};

export const validateExpenses = (expenses) => {
  if (typeof expenses !== 'number' || expenses < 0) {
    return 'Expenses must be a non-negative number.';
  }
  return null;
};

export const validateSavings = (savings) => {
  if (typeof savings !== 'number' || savings < 0) {
    return 'Savings must be a non-negative number.';
  }
  return null;
};

export const validateTransactionAmount = (amount) => {
  if (typeof amount !== 'number' || amount <= 0) {
    return 'Transaction amount must be a positive number.';
  }
  return null;
};

export const validateTransactionDate = (date) => {
  const parsedDate = new Date(date);
  if (isNaN(parsedDate.getTime())) {
    return 'Invalid date format.';
  }
  return null;
};

export const validateGoalInput = (goal) => {
  if (typeof goal !== 'string' || goal.trim() === '') {
    return 'Goal must be a non-empty string.';
  }
  return null;
};