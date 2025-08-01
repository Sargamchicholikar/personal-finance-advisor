import { fetchInvestmentSuggestions, fetchPortfolioData } from './api';

export const getInvestmentSuggestions = async (userProfile) => {
  try {
    const suggestions = await fetchInvestmentSuggestions(userProfile);
    return suggestions;
  } catch (error) {
    console.error('Error fetching investment suggestions:', error);
    throw error;
  }
};

export const getPortfolioData = async (userId) => {
  try {
    const portfolioData = await fetchPortfolioData(userId);
    return portfolioData;
  } catch (error) {
    console.error('Error fetching portfolio data:', error);
    throw error;
  }
};

export const calculatePotentialReturns = (investmentAmount, rateOfReturn, years) => {
  return investmentAmount * Math.pow((1 + rateOfReturn / 100), years);
};

const investmentService = {
  getInvestmentSuggestions,
  getPortfolioData,
  calculatePotentialReturns
};

export default investmentService;