import React from 'react';
import styles from './Education.module.css';

const glossaryTerms = [
  { term: 'Budget', definition: 'A plan for managing income and expenses over a specific period.' },
  { term: 'Savings', definition: 'Money that is set aside for future use, typically in a savings account.' },
  { term: 'Investment', definition: 'The act of allocating resources, usually money, in order to generate income or profit.' },
  { term: 'Emergency Fund', definition: 'A savings account that is used for unexpected expenses or emergencies.' },
  { term: 'Debt', definition: 'Money that is owed to another party, often with interest.' },
  { term: 'Asset', definition: 'Any resource owned by an individual or entity that has economic value.' },
  { term: 'Liability', definition: 'A financial obligation or debt that an individual or entity owes to another party.' },
  { term: 'Net Worth', definition: 'The difference between total assets and total liabilities.' },
  { term: 'Diversification', definition: 'A risk management strategy that mixes a wide variety of investments within a portfolio.' },
  { term: 'Risk Tolerance', definition: 'An investor’s ability and willingness to lose some or all of their original investment in exchange for greater potential returns.' },
];

const Glossary = () => {
  return (
    <div className={styles.glossaryContainer}>
      <h2 className={styles.glossaryTitle}>Financial Glossary</h2>
      <ul className={styles.glossaryList}>
        {glossaryTerms.map((item, index) => (
          <li key={index} className={styles.glossaryItem}>
            <strong>{item.term}:</strong> {item.definition}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Glossary;