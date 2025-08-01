import { fetchEducationalContent, fetchFinancialTips, fetchGlossaryTerms } from './api';

export const getEducationalContent = async () => {
  try {
    const content = await fetchEducationalContent();
    return content;
  } catch (error) {
    console.error('Error fetching educational content:', error);
    throw error;
  }
};

export const getFinancialTips = async () => {
  try {
    const tips = await fetchFinancialTips();
    return tips;
  } catch (error) {
    console.error('Error fetching financial tips:', error);
    throw error;
  }
};

export const getGlossaryTerms = async () => {
  try {
    const terms = await fetchGlossaryTerms();
    return terms;
  } catch (error) {
    console.error('Error fetching glossary terms:', error);
    throw error;
  }
};