import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import PersonalFinanceChatbot from './PersonalFinanceChatbot';
import PersonalFinanceAdvisorSimple from './PersonalFinanceAdvisorSimple';
import SimpleTest from './SimpleTest';
import TestingInterface from './tests/TestingInterface';

const App = () => {
  return (
    <Router>
      <Switch>
        <Route path="/app" component={PersonalFinanceAdvisorSimple} />
        <Route path="/test" component={SimpleTest} />
        <Route path="/testing" component={TestingInterface} />
        <Route path="/" exact component={PersonalFinanceChatbot} />
      </Switch>
    </Router>
  );
};

export default App;