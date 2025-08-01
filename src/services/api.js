import axios from 'axios';

const API_BASE_URL = 'https://api.personalfinanceadvisor.com'; // Replace with your actual API base URL

// User Profile API calls
export const fetchUserProfile = async (userId) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/users/${userId}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching user profile:', error);
    throw error;
  }
};

export const updateUserProfile = async (userId, profileData) => {
  try {
    const response = await axios.put(`${API_BASE_URL}/users/${userId}`, profileData);
    return response.data;
  } catch (error) {
    console.error('Error updating user profile:', error);
    throw error;
  }
};

// Budget API calls
export const fetchBudgets = async (userId) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/users/${userId}/budgets`);
    return response.data;
  } catch (error) {
    console.error('Error fetching budgets:', error);
    throw error;
  }
};

export const createBudget = async (userId, budgetData) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/users/${userId}/budgets`, budgetData);
    return response.data;
  } catch (error) {
    console.error('Error creating budget:', error);
    throw error;
  }
};

// Transaction API calls
export const fetchTransactions = async (userId) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/users/${userId}/transactions`);
    return response.data;
  } catch (error) {
    console.error('Error fetching transactions:', error);
    throw error;
  }
};

export const addTransaction = async (userId, transactionData) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/users/${userId}/transactions`, transactionData);
    return response.data;
  } catch (error) {
    console.error('Error adding transaction:', error);
    throw error;
  }
};

// Education API calls
export const fetchEducationalContent = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/education`);
    return response.data;
  } catch (error) {
    console.error('Error fetching educational content:', error);
    throw error;
  }
};

// Analytics API calls
export const fetchFinancialReports = async (userId) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/users/${userId}/analytics/reports`);
    return response.data;
  } catch (error) {
    console.error('Error fetching financial reports:', error);
    throw error;
  }
};

// AI Bot Response API call with enhanced conversational responses
export const getBotResponse = async (message, userProfile = {}, conversationHistory = []) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/chat/bot-response`, {
      message,
      userProfile,
      conversationHistory
    });
    return response.data.message;
  } catch (error) {
    console.error('Error getting bot response:', error);
    // Dynamic contextual responses instead of static templates
    return generateContextualResponse(message, userProfile, conversationHistory);
  }
};

const generateContextualResponse = (message, userProfile, conversationHistory = []) => {
  const lowerMessage = message.toLowerCase();
  const lastMessages = conversationHistory.slice(-3); // Get last 3 messages for context
  const userSaidNumbers = message.match(/\d+/g);
  const amount = userSaidNumbers ? parseFloat(userSaidNumbers[0]) : null;
  
  // Analyze conversation flow
  const isFollowUp = lastMessages.some(msg => 
    msg.sender === 'bot' && (
      msg.text.includes('?') || 
      msg.text.includes('tell me') || 
      msg.text.includes('what')
    )
  );
  
  // Extract intent and context
  const hasGreeting = lowerMessage.match(/^(hi|hello|hey|sup|what's up)/);
  const askingAbout = lowerMessage.match(/how do i|how can i|what should i|should i|can you help|tell me about/);
  const expressing = lowerMessage.match(/i'm|i am|i have|i want|i need|i earn|i make|i owe|i spend/);
  
  // Contextual greeting responses
  if (hasGreeting) {
    const timeOfDay = new Date().getHours() < 12 ? 'morning' : new Date().getHours() < 17 ? 'afternoon' : 'evening';
    const responses = [
      `Good ${timeOfDay}! I'm your personal finance assistant. What's on your financial mind today?`,
      `Hey there! Ready to make some smart money moves? What can I help you with?`,
      `Hi! Whether it's budgeting, saving, investing, or paying off debt - I'm here to help. What's your question?`,
      `Hello! I'm here to give you personalized financial advice. What would you like to work on today?`
    ];
    return responses[Math.floor(Math.random() * responses.length)];
  }
  
  // Dynamic number-based responses
  if (amount && expressing) {
    if (lowerMessage.includes('make') || lowerMessage.includes('earn') || lowerMessage.includes('income')) {
      // Check if it's annual income and convert to monthly
      const isAnnual = lowerMessage.includes('annual') || lowerMessage.includes('yearly') || lowerMessage.includes('year') || lowerMessage.includes('per year');
      const monthly = isAnnual ? Math.round(amount / 12) : amount;
      const needs = Math.round(monthly * 0.5);
      const wants = Math.round(monthly * 0.3);
      const savings = Math.round(monthly * 0.2);
      
      return `Perfect! With $${monthly.toLocaleString()} monthly income, here's your personalized financial roadmap:

🏠 **Essentials (50%)**: $${needs.toLocaleString()}
   Housing, utilities, groceries, minimum debt payments, transportation

🎯 **Lifestyle (30%)**: $${wants.toLocaleString()}
   Dining out, entertainment, hobbies, subscriptions, shopping

💰 **Future You (20%)**: $${savings.toLocaleString()}
   Emergency fund, retirement, investments, extra debt payments

Quick questions to optimize this further:
• What's your biggest expense right now?
• Do you have any debt I should factor in?
• Any specific financial goals you're working toward?`;
    }
    
    if (lowerMessage.includes('debt') || lowerMessage.includes('owe') || lowerMessage.includes('credit card')) {
      const interestRate = lowerMessage.includes('credit') ? 22 : lowerMessage.includes('student') ? 6 : 15;
      const monthlyInterest = Math.round((amount * (interestRate / 100)) / 12);
      const aggressivePayment = userProfile.income ? Math.min(amount * 0.1, userProfile.income * 0.15) : amount * 0.1;
      const monthsToPayoff = Math.ceil(amount / aggressivePayment);
      
      return `$${amount.toLocaleString()} in debt? Let's create your payoff strategy!

💸 **Current situation**:
   You're paying ~$${monthlyInterest}/month just in interest (assuming ${interestRate}% rate)
   
🎯 **Your action plan**:
   ${userProfile.income ? `With your $${userProfile.income.toLocaleString()} income, ` : ''}Pay $${Math.round(aggressivePayment).toLocaleString()}/month
   → You'd be debt-free in ${monthsToPayoff} months!
   → Save $${Math.round(monthlyInterest * monthsToPayoff - amount).toLocaleString()} in interest

🚀 **Quick wins to accelerate**:
   • Side hustle for extra payments
   • Sell items you don't need
   • Use tax refunds/bonuses for principal

What's the actual interest rate? And are there any other debts I should know about?`;
    }
    
    if (lowerMessage.includes('save') || lowerMessage.includes('saving')) {
      const timeframe = lowerMessage.match(/(\d+)\s*(month|year)/);
      const months = timeframe ? 
        (timeframe[2] === 'year' ? parseInt(timeframe[1]) * 12 : parseInt(timeframe[1])) : 12;
      const monthlyNeeded = Math.ceil(amount / months);
      
      return `Saving $${amount.toLocaleString()} is a fantastic goal! ${timeframe ? `To reach this in ${timeframe[0]}, you'll need to save $${monthlyNeeded.toLocaleString()}/month.` : ''}

🎯 **Your savings strategy**:
   ${userProfile.income ? 
     `That's ${Math.round((monthlyNeeded / userProfile.income) * 100)}% of your monthly income - ${monthlyNeeded / userProfile.income > 0.2 ? 'ambitious but doable with the right plan!' : 'very achievable!'}` : 
     'Let\'s make this automatic!'}

💰 **Action steps**:
   1. Open high-yield savings (4-5% APY)
   2. Automate weekly transfers of $${Math.ceil(monthlyNeeded / 4).toLocaleString()}
   3. Save windfalls (tax refunds, bonuses, gifts)
   4. Try the 52-week challenge for extra motivation

What's this money for? Emergency fund, vacation, house down payment? That'll help me give you more specific advice!`;
    }
    
    if (lowerMessage.includes('invest') || lowerMessage.includes('investment')) {
      const conservative = Math.round(amount * Math.pow(1.06, 10));
      const moderate = Math.round(amount * Math.pow(1.08, 10));
      const aggressive = Math.round(amount * Math.pow(1.12, 10));
      
      return `Investing $${amount.toLocaleString()} is smart! Your money could grow to:

📈 **10-year projections**:
   🛡️ Conservative (6%): $${conservative.toLocaleString()}
   ⚖️ Balanced (8%): $${moderate.toLocaleString()}
   🚀 Aggressive (12%): $${aggressive.toLocaleString()}

💡 **My recommendation**:
   ${amount < 1000 ? 
     'Start with broad market index funds (VTI, VTSAX) - simple, diversified, low fees' :
     amount < 10000 ?
     'Split between index funds (70%) and individual stocks (30%) for growth potential' :
     'Consider target-date funds or a three-fund portfolio for hands-off investing'}

⚠️ **First, quick check**:
   • Do you have 3-6 months expenses saved? (Emergency fund first!)
   • Any high-interest debt? (Pay off credit cards first - guaranteed 20%+ return!)
   
How long are you planning to invest this money?`;
    }
  }
  
  // Question-based responses
  if (askingAbout) {
    if (lowerMessage.includes('budget')) {
      return `Creating a budget that actually works? Here's my step-by-step approach:

🔍 **Step 1: Know your money**
   Track spending for one week - use your bank app or write it down
   
📊 **Step 2: The 50/30/20 rule** ${userProfile.income ? `(based on your $${userProfile.income.toLocaleString()} income)` : ''}
   ${userProfile.income ? 
     `• Needs: $${Math.round(userProfile.income * 0.5).toLocaleString()} - rent, utilities, groceries
   • Wants: $${Math.round(userProfile.income * 0.3).toLocaleString()} - fun stuff, dining out
   • Savings: $${Math.round(userProfile.income * 0.2).toLocaleString()} - future you!` :
     '• 50% needs, 30% wants, 20% savings'}

🎯 **Step 3: Make it automatic**
   Set up separate accounts and automatic transfers
   
Want me to help you customize this based on your specific situation? What's your biggest spending category?`;
    }
    
    if (lowerMessage.includes('save money') || lowerMessage.includes('cut expenses')) {
      return `Ready to find some money in your budget? Here are proven tactics that actually work:

💡 **Quick wins (save $200-500/month)**:
   📱 Cancel unused subscriptions (check your bank statement!)
   🛒 Meal prep instead of eating out (save $300+/month)
   ☕ Make coffee at home (save $100+/month)
   🚗 Combine errands to save on gas
   
💰 **Bigger moves (save $500+/month)**:
   🏠 Refinance mortgage or find cheaper rent
   📞 Call providers to negotiate bills (internet, phone, insurance)
   🎬 Switch to cheaper streaming services
   🏋️ Use free workouts instead of gym membership
   
🎯 **The 30-day rule**: For any non-essential purchase over $50, wait 30 days
   
Which area do you think has the most potential for savings in your budget?`;
    }
    
    if (lowerMessage.includes('start investing') || lowerMessage.includes('invest')) {
      return `Great question! Here's your beginner-friendly investing roadmap:

✅ **Before you invest (Foundation first!)**:
   1. Emergency fund: 3-6 months expenses ✓
   2. High-interest debt paid off ✓ 
   3. Employer 401k match ✓
   
📈 **Your first investments**:
   🥇 **Target-date fund**: Set it and forget it (Vanguard, Fidelity)
   🥈 **Index funds**: Total stock market (VTI) + bonds (BND)
   🥉 **Individual stocks**: Start with 5-10% of portfolio
   
💰 **How much to start**:
   Many brokers have $0 minimums - you can start with $100!
   Aim for 10-15% of income long-term
   
🎯 **My beginner strategy**:
   Start with $100/month into a target-date fund
   Increase by $50 every 6 months
   
Do you have your emergency fund and high-interest debt handled? That's step one!`;
    }
  }
  
  // Personal situation responses
  if (expressing) {
    if (lowerMessage.includes('struggling') || lowerMessage.includes('tight') || lowerMessage.includes('broke')) {
      return `I hear you - financial stress is real and you're not alone. Let's tackle this step by step.

🆘 **Immediate help**:
   • Local food banks and assistance programs
   • Negotiate payment plans with creditors
   • Side gigs for quick cash (DoorDash, TaskRabbit, etc.)
   
📋 **Let's triage your situation**:
   1. List all income sources
   2. List all essential expenses (rent, utilities, food, minimum debt payments)
   3. Find the gap and prioritize what to cut/earn
   
💪 **You've got this because**:
   This is temporary - small changes add up to big improvements
   There are always options, even when it doesn't feel like it
   
What's the most urgent financial issue right now? Rent, utilities, debt payments, or something else? Let's solve one thing at a time.`;
    }
    
    if (lowerMessage.includes('good') || lowerMessage.includes('comfortable') || lowerMessage.includes('stable')) {
      return `That's awesome that you're in a stable spot! Now's the perfect time to level up your financial game.

🚀 **Optimization opportunities**:
   • Max out retirement accounts (401k, IRA)
   • Build wealth through investing
   • Plan for major goals (house, travel, early retirement)
   • Optimize taxes and insurance
   
🎯 **Next level moves**:
   • Increase emergency fund to 6-12 months
   • Diversify income streams
   • Consider real estate investing
   • Estate planning and life insurance
   
💰 **The wealth-building formula**:
   High savings rate + consistent investing + time = financial freedom
   
What's your biggest financial goal for the next 2-3 years? Let's create a specific plan to get you there!`;
    }
  }
  
  // Follow-up responses based on conversation context
  if (isFollowUp && lastMessages.length > 0) {
    const lastBotMessage = lastMessages.find(msg => msg.sender === 'bot')?.text || '';
    
    if (lastBotMessage.includes('income') && amount) {
      return `Got it! $${amount.toLocaleString()} income changes everything. Let me recalculate your personalized plan...

With this income level, you're in ${amount > 8000 ? 'excellent' : amount > 5000 ? 'good' : 'manageable'} shape to build wealth.

Your optimized budget:
• Essentials: $${Math.round(amount * 0.5).toLocaleString()}
• Lifestyle: $${Math.round(amount * 0.3).toLocaleString()} 
• Wealth building: $${Math.round(amount * 0.2).toLocaleString()}

What's your current biggest expense? That's usually where we can find the most optimization opportunities.`;
    }
    
    if (lastBotMessage.includes('debt') && lowerMessage.includes('yes')) {
      return `Alright, let's tackle that debt strategically! Here's what I need to create your personalized payoff plan:

📝 **Debt inventory**:
   • What types? (credit cards, student loans, car, etc.)
   • Interest rates for each?
   • Minimum payments?
   
🎯 **Strategy options**:
   • **Avalanche**: Pay minimums + extra on highest rate (saves most money)
   • **Snowball**: Pay minimums + extra on smallest balance (builds momentum)
   
💡 **Acceleration tactics**:
   • Balance transfers to 0% APR cards
   • Debt consolidation loans
   • Side hustle income dedicated to debt
   
Give me the details and I'll run the numbers to show you exactly when you'll be debt-free!`;
    }
  }
  
  // Context-aware clarifying questions
  if (lowerMessage.length < 10 || lowerMessage.includes('help') || lowerMessage.includes('what')) {
    const clarifyingQuestions = [
      "I'd love to help! Could you be more specific? For example: 'How should I budget my $5000 income?' or 'What's the best way to pay off $3000 in credit card debt?'",
      "Tell me more about your situation! Are you looking to save money, pay off debt, start investing, or something else?",
      "Let's get specific so I can give you actionable advice! What's your main financial challenge or goal right now?",
      "I'm here to help with budgeting, saving, investing, debt payoff, or any money question. What's on your mind?"
    ];
    return clarifyingQuestions[Math.floor(Math.random() * clarifyingQuestions.length)];
  }
  
  // Thank you responses
  if (lowerMessage.includes('thank') || lowerMessage.includes('thanks')) {
    const responses = [
      "You're so welcome! Feel free to ask me anything else about your finances.",
      "Happy to help! What's your next money question?",
      "My pleasure! I'm here whenever you need financial guidance.",
      "Glad I could help! Any other financial goals you want to tackle?"
    ];
    return responses[Math.floor(Math.random() * responses.length)];
  }
  
  // Default response with personality
  return `I want to give you the best possible advice! Could you tell me a bit more about your financial situation?

💭 **For example, try saying**:
   • "I make $5000/month and want to budget better"
   • "I have $2000 in credit card debt at 24% interest"  
   • "I want to invest $1000 but don't know how to start"
   • "I'm struggling to save money each month"

🎯 **Or ask about specific topics**:
   • Budgeting and expense tracking
   • Debt payoff strategies  
   • Investment and retirement planning
   • Saving for specific goals
   
The more details you share, the more personalized and helpful my advice will be!`;
};

// Investment API calls
export const fetchInvestmentSuggestions = async (userProfile) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/investments/suggestions`, userProfile);
    return response.data;
  } catch (error) {
    console.error('Error fetching investment suggestions:', error);
    // Return fallback data for development
    return [
      { type: 'Low Risk', suggestion: 'Government Bonds', expectedReturn: '3-5%' },
      { type: 'Medium Risk', suggestion: 'Index Funds', expectedReturn: '7-10%' },
      { type: 'High Risk', suggestion: 'Individual Stocks', expectedReturn: '10-15%' }
    ];
  }
};

export const fetchPortfolioData = async (userId) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/users/${userId}/portfolio`);
    return response.data;
  } catch (error) {
    console.error('Error fetching portfolio data:', error);
    // Return fallback data for development
    return {
      totalValue: 10000,
      investments: [
        { name: 'Tech Index Fund', value: 5000, allocation: '50%' },
        { name: 'Government Bonds', value: 3000, allocation: '30%' },
        { name: 'Individual Stocks', value: 2000, allocation: '20%' }
      ]
    };
  }
};

// User data fetching function for analytics
export const fetchUserData = async (userId) => {
  try {
    const profile = await fetchUserProfile(userId);
    return { 
      profile, 
      chat: [] // Add any chat history if needed
    };
  } catch (error) {
    console.error('Error fetching user data:', error);
    throw error;
  }
};

// Personalized advice API call
export const getPersonalizedAdvice = async (userProfile) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/advice/personalized`, userProfile);
    return response.data;
  } catch (error) {
    console.error('Error fetching personalized advice:', error);
    // Return fallback advice for development
    return {
      advice: "Based on your financial profile, consider creating an emergency fund equal to 3-6 months of expenses, and diversify your investment portfolio to match your risk tolerance.",
      priority: "high",
      category: "savings"
    };
  }
};