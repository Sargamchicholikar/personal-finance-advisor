import React, { useState, useEffect } from 'react';
import styles from '../Education/Education.module.css';

const FinancialEducationHub = () => {
  const [currentLesson, setCurrentLesson] = useState(null);
  const [completedLessons, setCompletedLessons] = useState([]);
  const [quizScores, setQuizScores] = useState({});
  const [userLevel, setUserLevel] = useState('Beginner');

  const educationalContent = {
    beginner: [
      {
        id: 1,
        title: 'Budgeting Basics',
        content: `
          <h4>What is Budgeting?</h4>
          <p>Budgeting is creating a plan for how you'll spend your money each month. It helps you:</p>
          <ul>
            <li>Track where your money goes</li>
            <li>Ensure you can pay for necessities</li>
            <li>Save for future goals</li>
            <li>Avoid overspending</li>
          </ul>
          
          <h4>The 50/30/20 Rule</h4>
          <p>A simple budgeting method:</p>
          <ul>
            <li><strong>50%</strong> - Needs (rent, groceries, utilities)</li>
            <li><strong>30%</strong> - Wants (entertainment, dining out)</li>
            <li><strong>20%</strong> - Savings and debt repayment</li>
          </ul>
        `,
        quiz: [
          {
            question: "In the 50/30/20 rule, what percentage should go to savings?",
            options: ["10%", "20%", "30%", "50%"],
            correct: 1
          },
          {
            question: "Which is considered a 'need' in budgeting?",
            options: ["Netflix subscription", "Rent payment", "Restaurant meals", "New clothes"],
            correct: 1
          }
        ],
        practicalTip: "Start by tracking your expenses for one week to understand your spending patterns."
      },
      {
        id: 2,
        title: 'Understanding Interest',
        content: `
          <h4>Simple vs Compound Interest</h4>
          <p><strong>Simple Interest:</strong> Interest calculated only on the principal amount.</p>
          <p>Formula: Interest = Principal × Rate × Time</p>
          
          <p><strong>Compound Interest:</strong> Interest calculated on principal plus previously earned interest.</p>
          <p>This is the "interest on interest" that makes your money grow faster over time.</p>
          
          <h4>The Power of Compound Interest</h4>
          <p>Albert Einstein allegedly called compound interest "the eighth wonder of the world."</p>
          <p>Example: $1,000 invested at 7% annual interest:</p>
          <ul>
            <li>After 10 years: $1,967</li>
            <li>After 20 years: $3,870</li>
            <li>After 30 years: $7,612</li>
          </ul>
        `,
        quiz: [
          {
            question: "Which type of interest grows faster over time?",
            options: ["Simple interest", "Compound interest", "Both are the same", "Neither"],
            correct: 1
          }
        ],
        practicalTip: "Start investing early, even small amounts, to take advantage of compound interest."
      },
      {
        id: 3,
        title: 'Emergency Funds',
        content: `
          <h4>Why You Need an Emergency Fund</h4>
          <p>Life is unpredictable. Emergency funds protect you from:</p>
          <ul>
            <li>Job loss</li>
            <li>Medical emergencies</li>
            <li>Car repairs</li>
            <li>Home maintenance issues</li>
          </ul>
          
          <h4>How Much to Save</h4>
          <p><strong>Minimum:</strong> $1,000 for small emergencies</p>
          <p><strong>Ideal:</strong> 3-6 months of living expenses</p>
          <p><strong>High-risk situations:</strong> 6-12 months (unstable job, health issues)</p>
          
          <h4>Where to Keep Your Emergency Fund</h4>
          <ul>
            <li>High-yield savings account</li>
            <li>Money market account</li>
            <li>Short-term CD (Certificate of Deposit)</li>
          </ul>
        `,
        quiz: [
          {
            question: "How much should you ideally have in an emergency fund?",
            options: ["1 month expenses", "3-6 months expenses", "1 year expenses", "$100"],
            correct: 1
          }
        ],
        practicalTip: "Start with $25/month. Automate transfers to make saving easier."
      }
    ],
    intermediate: [
      {
        id: 4,
        title: 'Investment Basics',
        content: `
          <h4>Types of Investments</h4>
          <p><strong>Stocks:</strong> Ownership shares in companies. Higher risk, higher potential return.</p>
          <p><strong>Bonds:</strong> Loans to companies or governments. Lower risk, steady returns.</p>
          <p><strong>Mutual Funds:</strong> Pools of money invested in various stocks/bonds.</p>
          <p><strong>ETFs:</strong> Exchange-traded funds that track indexes.</p>
          
          <h4>Risk vs Return</h4>
          <p>Generally, higher potential returns come with higher risk.</p>
          <ul>
            <li>Savings accounts: Low risk, low return (1-2%)</li>
            <li>Bonds: Medium risk, medium return (3-5%)</li>
            <li>Stocks: High risk, high return (7-10% historical average)</li>
          </ul>
          
          <h4>Diversification</h4>
          <p>"Don't put all your eggs in one basket." Spread investments across:</p>
          <ul>
            <li>Different asset types (stocks, bonds, real estate)</li>
            <li>Different companies and industries</li>
            <li>Different geographic regions</li>
          </ul>
        `,
        quiz: [
          {
            question: "What is diversification in investing?",
            options: ["Buying only one stock", "Spreading investments across different assets", "Timing the market", "Day trading"],
            correct: 1
          }
        ],
        practicalTip: "Start with low-cost index funds for instant diversification."
      }
    ],
    advanced: [
      {
        id: 5,
        title: 'Tax-Advantaged Accounts',
        content: `
          <h4>Types of Retirement Accounts</h4>
          <p><strong>401(k):</strong> Employer-sponsored retirement account</p>
          <ul>
            <li>Pre-tax contributions (traditional) or after-tax (Roth)</li>
            <li>Often includes employer matching</li>
            <li>Annual limit: $22,500 (2023)</li>
          </ul>
          
          <p><strong>IRA (Individual Retirement Account):</strong></p>
          <ul>
            <li>Traditional IRA: Tax-deductible contributions, taxed on withdrawal</li>
            <li>Roth IRA: After-tax contributions, tax-free growth and withdrawals</li>
            <li>Annual limit: $6,500 (2023)</li>
          </ul>
          
          <h4>Tax Strategy</h4>
          <p>Consider your current vs future tax bracket:</p>
          <ul>
            <li>Higher tax bracket now → Traditional 401(k)/IRA</li>
            <li>Lower tax bracket now → Roth 401(k)/IRA</li>
          </ul>
        `,
        quiz: [
          {
            question: "What's a key benefit of a Roth IRA?",
            options: ["Tax deduction now", "Tax-free withdrawals in retirement", "No contribution limits", "Guaranteed returns"],
            correct: 1
          }
        ],
        practicalTip: "Always contribute enough to get full employer 401(k) matching - it's free money!"
      }
    ]
  };

  const glossaryTerms = [
    {
      term: "Asset Allocation",
      definition: "The strategy of dividing investments among different asset categories like stocks, bonds, and cash."
    },
    {
      term: "Bull Market",
      definition: "A period of rising stock prices, typically lasting months or years."
    },
    {
      term: "Bear Market",
      definition: "A period of declining stock prices, usually defined as a 20% drop from recent highs."
    },
    {
      term: "Dividend",
      definition: "A payment made by companies to shareholders, usually quarterly."
    },
    {
      term: "Expense Ratio",
      definition: "The annual fee charged by mutual funds or ETFs, expressed as a percentage."
    },
    {
      term: "Market Cap",
      definition: "The total value of a company's shares in the stock market."
    },
    {
      term: "P/E Ratio",
      definition: "Price-to-Earnings ratio, a valuation metric comparing stock price to earnings per share."
    },
    {
      term: "Volatility",
      definition: "The degree of variation in a trading price series over time."
    }
  ];

  useEffect(() => {
    loadProgress();
  }, []);

  const loadProgress = () => {
    const completed = JSON.parse(localStorage.getItem('completedLessons') || '[]');
    const scores = JSON.parse(localStorage.getItem('quizScores') || '{}');
    setCompletedLessons(completed);
    setQuizScores(scores);
    
    // Determine user level based on completed lessons
    if (completed.length >= 5) setUserLevel('Advanced');
    else if (completed.length >= 3) setUserLevel('Intermediate');
    else setUserLevel('Beginner');
  };

  const saveProgress = (lessonId, score = null) => {
    const newCompleted = [...completedLessons];
    if (!newCompleted.includes(lessonId)) {
      newCompleted.push(lessonId);
    }
    
    setCompletedLessons(newCompleted);
    localStorage.setItem('completedLessons', JSON.stringify(newCompleted));
    
    if (score !== null) {
      const newScores = { ...quizScores, [lessonId]: score };
      setQuizScores(newScores);
      localStorage.setItem('quizScores', JSON.stringify(newScores));
    }
  };

  const takeQuiz = (lesson) => {
    const quiz = lesson.quiz;
    let score = 0;
    const answers = [];

    quiz.forEach((question, index) => {
      const answer = prompt(`${question.question}\n${question.options.map((opt, i) => `${i + 1}. ${opt}`).join('\n')}\n\nEnter number (1-4):`);
      const answerIndex = parseInt(answer) - 1;
      answers.push(answerIndex);
      if (answerIndex === question.correct) {
        score++;
      }
    });

    const percentage = (score / quiz.length) * 100;
    alert(`Quiz Complete!\nScore: ${score}/${quiz.length} (${percentage.toFixed(1)}%)`);
    
    saveProgress(lesson.id, percentage);
    
    if (percentage >= 70) {
      alert("Great job! You can move on to the next lesson.");
    } else {
      alert("Consider reviewing the lesson material before moving forward.");
    }
  };

  const getAllLessons = () => {
    return [
      ...educationalContent.beginner,
      ...educationalContent.intermediate,
      ...educationalContent.advanced
    ];
  };

  return (
    <div className={styles.educationHub}>
      <h3 className={styles.sectionTitle}>🎓 Financial Education Hub</h3>
      
      {/* User Progress */}
      <div className={styles.progressSection}>
        <div className={styles.userLevel}>
          Current Level: <span className={styles.levelBadge}>{userLevel}</span>
        </div>
        <div className={styles.progressStats}>
          <span>Lessons Completed: {completedLessons.length}/{getAllLessons().length}</span>
          <div className={styles.progressBar}>
            <div 
              className={styles.progressFill}
              style={{ width: `${(completedLessons.length / getAllLessons().length) * 100}%` }}
            />
          </div>
        </div>
      </div>

      {/* Lesson Browser */}
      <div className={styles.lessonBrowser}>
        <h4>Available Lessons</h4>
        {Object.entries(educationalContent).map(([level, lessons]) => (
          <div key={level} className={styles.levelSection}>
            <h5 className={styles.levelTitle}>
              {level.charAt(0).toUpperCase() + level.slice(1)} Level
            </h5>
            <div className={styles.lessonGrid}>
              {lessons.map(lesson => (
                <div 
                  key={lesson.id} 
                  className={`${styles.lessonCard} ${completedLessons.includes(lesson.id) ? styles.completed : ''}`}
                  onClick={() => setCurrentLesson(lesson)}
                >
                  <h6>{lesson.title}</h6>
                  <div className={styles.lessonStatus}>
                    {completedLessons.includes(lesson.id) ? (
                      <span className={styles.completedBadge}>
                        ✓ Completed {quizScores[lesson.id] ? `(${quizScores[lesson.id].toFixed(0)}%)` : ''}
                      </span>
                    ) : (
                      <span className={styles.incompleteBadge}>Start Lesson</span>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>

      {/* Lesson Viewer */}
      {currentLesson && (
        <div className={styles.lessonViewer}>
          <div className={styles.lessonHeader}>
            <h4>{currentLesson.title}</h4>
            <button 
              onClick={() => setCurrentLesson(null)}
              className={styles.closeButton}
            >
              ✕
            </button>
          </div>
          
          <div 
            className={styles.lessonContent}
            dangerouslySetInnerHTML={{ __html: currentLesson.content }}
          />
          
          <div className={styles.practicalTip}>
            <strong>💡 Practical Tip:</strong> {currentLesson.practicalTip}
          </div>
          
          <div className={styles.lessonActions}>
            <button 
              onClick={() => takeQuiz(currentLesson)}
              className={styles.quizButton}
            >
              Take Quiz
            </button>
            <button 
              onClick={() => saveProgress(currentLesson.id)}
              className={styles.completeButton}
            >
              Mark as Complete
            </button>
          </div>
        </div>
      )}

      {/* Financial Glossary */}
      <div className={styles.glossarySection}>
        <h4>📚 Financial Glossary</h4>
        <div className={styles.glossaryGrid}>
          {glossaryTerms.map((item, index) => (
            <div key={index} className={styles.glossaryItem}>
              <div className={styles.glossaryTerm}>{item.term}</div>
              <div className={styles.glossaryDefinition}>{item.definition}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Quick Tips */}
      <div className={styles.quickTips}>
        <h4>💭 Quick Daily Tips</h4>
        <div className={styles.tipsList}>
          <div className={styles.tip}>💳 Pay off credit card balances in full each month to avoid interest charges.</div>
          <div className={styles.tip}>🏦 Check your credit report annually for free at annualcreditreport.com.</div>
          <div className={styles.tip}>📱 Use budgeting apps to track spending automatically.</div>
          <div className={styles.tip}>🎯 Set specific, measurable financial goals with deadlines.</div>
          <div className={styles.tip}>💰 Automate savings transfers to "pay yourself first."</div>
        </div>
      </div>
    </div>
  );
};

export default FinancialEducationHub;
