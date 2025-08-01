#!/usr/bin/env node

// Simple Console Test Script for Personal Finance Advisor
// Run with: node test-console.js

const { getBotResponse } = require('./src/services/api');

const testCases = [
  {
    name: "Income Test",
    input: "I make $5000 per month",
    expectation: "Should provide 50/30/20 budget breakdown"
  },
  {
    name: "Debt Test", 
    input: "I have $3000 in credit card debt",
    expectation: "Should provide debt payoff strategy"
  },
  {
    name: "Savings Test",
    input: "I want to save $10000 for a house",
    expectation: "Should provide savings timeline and strategy"
  },
  {
    name: "Investment Test",
    input: "How should I invest $5000?",
    expectation: "Should provide investment recommendations"
  },
  {
    name: "Greeting Test",
    input: "Hello",
    expectation: "Should provide friendly greeting"
  }
];

async function runConsoleTests() {
  console.log('🧪 Personal Finance Advisor Console Tests\n');
  console.log('==========================================\n');
  
  let passedTests = 0;
  const totalTests = testCases.length;
  
  for (const testCase of testCases) {
    console.log(`📝 Test: ${testCase.name}`);
    console.log(`💭 Input: "${testCase.input}"`);
    console.log(`🎯 Expected: ${testCase.expectation}`);
    
    try {
      const startTime = Date.now();
      const response = await getBotResponse(testCase.input, {}, []);
      const endTime = Date.now();
      const responseTime = endTime - startTime;
      
      console.log(`💬 Response (${responseTime}ms):`);
      console.log(`   ${response.substring(0, 150)}...`);
      
      // Simple validation
      const hasRelevantContent = response.length > 50 && !response.includes('I\'m here to help with all your financial questions');
      
      if (hasRelevantContent) {
        console.log('✅ PASSED\n');
        passedTests++;
      } else {
        console.log('❌ FAILED - Generic response\n');
      }
      
    } catch (error) {
      console.log(`❌ FAILED - Error: ${error.message}\n`);
    }
  }
  
  console.log('==========================================');
  console.log(`📊 Results: ${passedTests}/${totalTests} tests passed`);
  console.log(`📈 Success Rate: ${((passedTests/totalTests) * 100).toFixed(1)}%`);
  
  if (passedTests === totalTests) {
    console.log('🎉 All tests passed! Your chatbot is working great!');
  } else if (passedTests >= totalTests * 0.8) {
    console.log('✅ Most tests passed. Good performance!');
  } else {
    console.log('⚠️  Some tests failed. Check the responses above.');
  }
}

// Run tests if this file is executed directly
if (require.main === module) {
  runConsoleTests().catch(console.error);
}

module.exports = { runConsoleTests };
