// Personal Finance Advisor Test Suite
import { getBotResponse } from '../services/api';

class FinanceAdvisorTester {
  constructor() {
    this.testResults = [];
    this.userProfile = {
      income: 0,
      expenses: 0,
      savings: 0,
      debt: 0,
      goals: [],
      conversationContext: {}
    };
  }

  async runTest(name, input, expectedBehavior) {
    console.log(`\n🧪 Testing: ${name}`);
    console.log(`📝 Input: "${input}"`);
    
    try {
      const response = await getBotResponse(input, this.userProfile, []);
      const passed = this.validateResponse(response, expectedBehavior);
      
      this.testResults.push({
        name,
        input,
        response,
        expectedBehavior,
        passed,
        timestamp: new Date().toISOString()
      });

      console.log(`💬 Response: "${response.substring(0, 100)}..."`);
      console.log(`✅ Expected: ${expectedBehavior}`);
      console.log(`${passed ? '✅ PASSED' : '❌ FAILED'}`);
      
      return passed;
    } catch (error) {
      console.log(`❌ ERROR: ${error.message}`);
      return false;
    }
  }

  validateResponse(response, expectedBehavior) {
    const lowerResponse = response.toLowerCase();
    
    switch (expectedBehavior) {
      case 'greeting':
        return lowerResponse.includes('hi') || lowerResponse.includes('hello') || 
               lowerResponse.includes('hey') || lowerResponse.includes('welcome');
      
      case 'budget_calculation':
        return lowerResponse.includes('%') && lowerResponse.includes('$') &&
               (lowerResponse.includes('50') || lowerResponse.includes('30') || lowerResponse.includes('20'));
      
      case 'debt_strategy':
        return lowerResponse.includes('debt') && lowerResponse.includes('pay') &&
               (lowerResponse.includes('month') || lowerResponse.includes('interest') || lowerResponse.includes('strategy'));
      
      case 'savings_plan':
        return lowerResponse.includes('save') && lowerResponse.includes('$') &&
               (lowerResponse.includes('month') || lowerResponse.includes('goal') || lowerResponse.includes('plan'));
      
      case 'investment_advice':
        return lowerResponse.includes('invest') && 
               (lowerResponse.includes('fund') || lowerResponse.includes('stock') || lowerResponse.includes('return'));
      
      case 'contextual_response':
        return response.length > 50 && !response.includes('I\'m here to help with all your financial questions');
      
      default:
        return response.length > 20;
    }
  }

  async runAllTests() {
    console.log('🚀 Starting Personal Finance Advisor Test Suite\n');
    
    // Greeting Tests
    await this.runTest('Basic Greeting', 'Hello', 'greeting');
    await this.runTest('Casual Greeting', 'Hey there!', 'greeting');
    
    // Income & Budget Tests
    await this.runTest('Income Declaration', 'I make $5000 per month', 'budget_calculation');
    await this.runTest('Income with Context', 'My monthly income is $4500 and I need help budgeting', 'budget_calculation');
    
    // Debt Management Tests
    await this.runTest('Credit Card Debt', 'I have $3000 in credit card debt', 'debt_strategy');
    await this.runTest('Student Loan', 'I owe $15000 in student loans', 'debt_strategy');
    
    // Savings Tests
    await this.runTest('House Savings Goal', 'I want to save $20000 for a house down payment', 'savings_plan');
    await this.runTest('Emergency Fund', 'How much should I save for emergency fund?', 'savings_plan');
    
    // Investment Tests
    await this.runTest('Investment Query', 'How should I invest $10000?', 'investment_advice');
    await this.runTest('Retirement Planning', 'Help me plan for retirement', 'investment_advice');
    
    // Contextual Tests
    await this.runTest('Complex Scenario', 'I make $6000/month, have $5000 debt, want to invest $1000', 'contextual_response');
    await this.runTest('Follow-up Question', 'What about my credit score?', 'contextual_response');
    
    this.printResults();
  }

  printResults() {
    console.log('\n📊 TEST RESULTS SUMMARY');
    console.log('========================');
    
    const passed = this.testResults.filter(test => test.passed).length;
    const total = this.testResults.length;
    const passRate = ((passed / total) * 100).toFixed(1);
    
    console.log(`✅ Passed: ${passed}/${total} (${passRate}%)`);
    console.log(`❌ Failed: ${total - passed}/${total}`);
    
    console.log('\n📋 Detailed Results:');
    this.testResults.forEach((test, index) => {
      console.log(`${index + 1}. ${test.name}: ${test.passed ? '✅' : '❌'}`);
    });
    
    if (passRate >= 80) {
      console.log('\n🎉 EXCELLENT! Your chatbot is performing well!');
    } else if (passRate >= 60) {
      console.log('\n⚠️  GOOD: Some improvements needed');
    } else {
      console.log('\n🔧 NEEDS WORK: Major improvements required');
    }
  }

  // Performance Tests
  async testPerformance() {
    console.log('\n⚡ Performance Testing...');
    
    const testCases = [
      'I make $5000 per month',
      'I have $10000 in debt',
      'How should I invest?',
      'Help me budget'
    ];
    
    const times = [];
    
    for (const testCase of testCases) {
      const startTime = performance.now();
      await getBotResponse(testCase, this.userProfile, []);
      const endTime = performance.now();
      const responseTime = endTime - startTime;
      times.push(responseTime);
      console.log(`📝 "${testCase}": ${responseTime.toFixed(0)}ms`);
    }
    
    const avgTime = times.reduce((a, b) => a + b, 0) / times.length;
    console.log(`📊 Average Response Time: ${avgTime.toFixed(0)}ms`);
    
    if (avgTime < 100) {
      console.log('🚀 EXCELLENT response times!');
    } else if (avgTime < 500) {
      console.log('✅ GOOD response times');
    } else {
      console.log('⚠️  Response times could be improved');
    }
  }

  // Edge Case Tests
  async testEdgeCases() {
    console.log('\n🎯 Edge Case Testing...');
    
    await this.runTest('Empty Message', '', 'contextual_response');
    await this.runTest('Very Long Message', 'I make $5000 per month and have $3000 in credit card debt at 24% interest and I want to save $10000 for a house down payment and also invest in stocks and bonds for retirement planning while paying off my student loans', 'contextual_response');
    await this.runTest('Numbers Only', '5000', 'contextual_response');
    await this.runTest('Special Characters', 'I make $5,000.00 per month!!!', 'budget_calculation');
    await this.runTest('Typos', 'I mke 5000 dolars per mont', 'contextual_response');
  }
}

// Export for use in tests
export default FinanceAdvisorTester;

// Usage example:
// const tester = new FinanceAdvisorTester();
// tester.runAllTests();
