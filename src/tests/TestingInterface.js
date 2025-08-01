import React, { useState } from 'react';
import FinanceAdvisorTester from './FinanceAdvisorTester';
import { getBotResponse } from '../services/api';
import styles from '../styles/FinanceAdvisor.module.css';

const TestingInterface = () => {
  const [testResults, setTestResults] = useState([]);
  const [isRunning, setIsRunning] = useState(false);
  const [manualInput, setManualInput] = useState('');
  const [manualResponse, setManualResponse] = useState('');

  const runAutomatedTests = async () => {
    setIsRunning(true);
    setTestResults([]);
    
    const tester = new FinanceAdvisorTester();
    
    // Override the test result storage to update our React state
    const originalTestResults = tester.testResults;
    tester.testResults = [];
    
    // Run tests with real-time updates
    await tester.runAllTests();
    await tester.testPerformance();
    await tester.testEdgeCases();
    
    setTestResults(tester.testResults);
    setIsRunning(false);
  };

  const testManualInput = async () => {
    if (!manualInput.trim()) return;
    
    try {
      const response = await getBotResponse(manualInput, {}, []);
      setManualResponse(response);
    } catch (error) {
      setManualResponse(`Error: ${error.message}`);
    }
  };

  const quickTests = [
    { name: 'Income Test', input: 'I make $5000 per month' },
    { name: 'Debt Test', input: 'I have $3000 in credit card debt' },
    { name: 'Savings Test', input: 'I want to save $10000 for a house' },
    { name: 'Investment Test', input: 'How should I invest $5000?' },
    { name: 'Budget Test', input: 'Help me create a budget' }
  ];

  const runQuickTest = async (input) => {
    setManualInput(input);
    const response = await getBotResponse(input, {}, []);
    setManualResponse(response);
  };

  return (
    <div style={{ padding: '2rem', fontFamily: 'Inter, sans-serif' }}>
      <h1>🧪 Personal Finance Advisor Testing Interface</h1>
      
      {/* Automated Testing Section */}
      <div style={{ marginBottom: '3rem', padding: '2rem', background: '#f8fafc', borderRadius: '12px' }}>
        <h2>🤖 Automated Testing</h2>
        <button 
          onClick={runAutomatedTests}
          disabled={isRunning}
          style={{
            padding: '1rem 2rem',
            background: isRunning ? '#94a3b8' : '#3182ce',
            color: 'white',
            border: 'none',
            borderRadius: '8px',
            cursor: isRunning ? 'not-allowed' : 'pointer',
            fontSize: '1rem',
            fontWeight: '600'
          }}
        >
          {isRunning ? '🔄 Running Tests...' : '▶️ Run All Tests'}
        </button>
        
        {testResults.length > 0 && (
          <div style={{ marginTop: '2rem' }}>
            <h3>📊 Test Results ({testResults.filter(t => t.passed).length}/{testResults.length} passed)</h3>
            <div style={{ maxHeight: '400px', overflowY: 'auto' }}>
              {testResults.map((test, index) => (
                <div 
                  key={index}
                  style={{
                    padding: '1rem',
                    margin: '0.5rem 0',
                    background: test.passed ? '#dcfce7' : '#fee2e2',
                    borderRadius: '8px',
                    border: `1px solid ${test.passed ? '#22c55e' : '#ef4444'}`
                  }}
                >
                  <div style={{ fontWeight: '600', marginBottom: '0.5rem' }}>
                    {test.passed ? '✅' : '❌'} {test.name}
                  </div>
                  <div style={{ fontSize: '0.875rem', color: '#6b7280' }}>
                    Input: "{test.input}"
                  </div>
                  <div style={{ fontSize: '0.875rem', color: '#6b7280', marginTop: '0.25rem' }}>
                    Response: "{test.response.substring(0, 100)}..."
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Quick Tests Section */}
      <div style={{ marginBottom: '3rem', padding: '2rem', background: '#f1f5f9', borderRadius: '12px' }}>
        <h2>⚡ Quick Tests</h2>
        <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
          {quickTests.map((test, index) => (
            <button
              key={index}
              onClick={() => runQuickTest(test.input)}
              style={{
                padding: '0.75rem 1.5rem',
                background: '#3182ce',
                color: 'white',
                border: 'none',
                borderRadius: '8px',
                cursor: 'pointer',
                fontSize: '0.875rem',
                fontWeight: '500'
              }}
            >
              {test.name}
            </button>
          ))}
        </div>
      </div>

      {/* Manual Testing Section */}
      <div style={{ padding: '2rem', background: '#fefefe', borderRadius: '12px', border: '1px solid #e2e8f0' }}>
        <h2>✋ Manual Testing</h2>
        <div style={{ display: 'flex', gap: '1rem', marginBottom: '1rem' }}>
          <input
            type="text"
            value={manualInput}
            onChange={(e) => setManualInput(e.target.value)}
            placeholder="Type your test message here..."
            style={{
              flex: 1,
              padding: '1rem',
              border: '1px solid #d1d5db',
              borderRadius: '8px',
              fontSize: '1rem'
            }}
            onKeyPress={(e) => e.key === 'Enter' && testManualInput()}
          />
          <button
            onClick={testManualInput}
            style={{
              padding: '1rem 2rem',
              background: '#059669',
              color: 'white',
              border: 'none',
              borderRadius: '8px',
              cursor: 'pointer',
              fontSize: '1rem',
              fontWeight: '600'
            }}
          >
            Test
          </button>
        </div>
        
        {manualResponse && (
          <div style={{
            padding: '1.5rem',
            background: '#f8fafc',
            borderRadius: '8px',
            border: '1px solid #e2e8f0',
            whiteSpace: 'pre-wrap',
            lineHeight: '1.6'
          }}>
            <strong>Response:</strong><br />
            {manualResponse}
          </div>
        )}
      </div>

      {/* Testing Guidelines */}
      <div style={{ marginTop: '3rem', padding: '2rem', background: '#fffbeb', borderRadius: '12px', border: '1px solid #f59e0b' }}>
        <h2>📋 Testing Guidelines</h2>
        <h3>Test These Scenarios:</h3>
        <ul style={{ lineHeight: '1.8' }}>
          <li><strong>Income Processing:</strong> "I make $5000 per month", "My income is $75,000 annually"</li>
          <li><strong>Debt Analysis:</strong> "I have $3000 in credit card debt", "I owe $15,000 in student loans"</li>
          <li><strong>Savings Goals:</strong> "I want to save $10,000 for a house", "Emergency fund goal"</li>
          <li><strong>Investment Advice:</strong> "How should I invest $5000?", "Retirement planning help"</li>
          <li><strong>Budget Questions:</strong> "Help me create a budget", "How should I allocate my income?"</li>
          <li><strong>Complex Scenarios:</strong> Multiple financial aspects in one message</li>
          <li><strong>Edge Cases:</strong> Very long messages, typos, special characters</li>
        </ul>
        
        <h3>What to Check:</h3>
        <ul style={{ lineHeight: '1.8' }}>
          <li>✅ <strong>Number Recognition:</strong> Does it extract amounts correctly?</li>
          <li>✅ <strong>Personalized Responses:</strong> Does it use your specific numbers in calculations?</li>
          <li>✅ <strong>Context Awareness:</strong> Does it remember previous conversation?</li>
          <li>✅ <strong>Professional Tone:</strong> Is the advice clear and actionable?</li>
          <li>✅ <strong>Response Time:</strong> Are responses quick (under 500ms)?</li>
        </ul>
      </div>
    </div>
  );
};

export default TestingInterface;
