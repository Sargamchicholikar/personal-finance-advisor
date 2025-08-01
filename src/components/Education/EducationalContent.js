import React from 'react';
import styles from './Education.module.css';

const EducationalContent = () => {
  return (
    <div className={styles.educationalContent}>
      <h2>Educational Resources</h2>
      <p>Welcome to the Educational Resources section! Here you will find various articles, lessons, and tips to enhance your financial knowledge.</p>
      
      <section>
        <h3>Financial Lessons</h3>
        <p>Explore our comprehensive lessons on personal finance topics, including budgeting, saving, investing, and more.</p>
      </section>

      <section>
        <h3>Tips and Tricks</h3>
        <p>Discover practical tips for managing your finances effectively and making informed financial decisions.</p>
      </section>

      <section>
        <h3>Glossary of Terms</h3>
        <p>Familiarize yourself with common financial terms to better understand the language of finance.</p>
      </section>

      <section>
        <h3>Additional Resources</h3>
        <p>Check out our recommended books, websites, and tools that can help you on your financial journey.</p>
      </section>
    </div>
  );
};

export default EducationalContent;