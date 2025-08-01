import React from 'react';

const SimpleTest = () => {
  return (
    <div style={{
      height: '100vh',
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      backgroundColor: '#f0f8ff',
      fontFamily: 'Arial, sans-serif'
    }}>
      <div style={{
        padding: '3rem',
        backgroundColor: 'white',
        borderRadius: '15px',
        boxShadow: '0 10px 30px rgba(0,0,0,0.1)',
        textAlign: 'center',
        maxWidth: '600px'
      }}>
        <h1 style={{ 
          color: '#2c3e50', 
          marginBottom: '1rem',
          fontSize: '2.5rem'
        }}>
          🏦 Personal Finance Advisor
        </h1>
        <p style={{ 
          color: '#666', 
          marginBottom: '2rem',
          fontSize: '1.2rem',
          lineHeight: '1.6'
        }}>
          Welcome to your comprehensive financial management platform!
          <br />
          <strong>React is working correctly!</strong>
        </p>
        
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(2, 1fr)',
          gap: '1rem',
          marginTop: '2rem'
        }}>
          <div style={{
            padding: '1rem',
            backgroundColor: '#e8f5e8',
            borderRadius: '8px',
            border: '2px solid #28a745'
          }}>
            <h3 style={{ color: '#28a745', margin: '0 0 0.5rem 0' }}>✅ App Status</h3>
            <p style={{ margin: 0, color: '#155724' }}>React Loading Successfully</p>
          </div>
          
          <div style={{
            padding: '1rem',
            backgroundColor: '#e3f2fd',
            borderRadius: '8px',
            border: '2px solid #2196f3'
          }}>
            <h3 style={{ color: '#2196f3', margin: '0 0 0.5rem 0' }}>🚀 Ready</h3>
            <p style={{ margin: 0, color: '#0d47a1' }}>Components Loading</p>
          </div>
        </div>
        
        <button 
          style={{
            marginTop: '2rem',
            padding: '1rem 2rem',
            backgroundColor: '#667eea',
            color: 'white',
            border: 'none',
            borderRadius: '8px',
            fontSize: '1.1rem',
            cursor: 'pointer',
            fontWeight: '600'
          }}
          onClick={() => {
            alert('React is working perfectly! ✅\n\nThe application framework is operational.\nAll components should load correctly.');
          }}
        >
          Test React Functionality
        </button>
      </div>
    </div>
  );
};

export default SimpleTest;
