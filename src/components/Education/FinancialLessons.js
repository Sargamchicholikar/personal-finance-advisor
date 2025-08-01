import React from 'react';
import styles from './Education.module.css';

const FinancialLessons = () => {
  const lessons = [
    {
      title: 'Understanding Budgeting',
      content: 'Budgeting is the process of creating a plan to spend your money. It helps you determine in advance whether you will have enough money to do the things you need or want to do.'
    },
    {
      title: 'The Importance of Saving',
      content: 'Saving money is essential for financial security. It allows you to prepare for emergencies, make large purchases, and invest in your future.'
    },
    {
      title: 'Investing Basics',
      content: 'Investing involves putting your money into assets with the expectation of generating a profit. Understanding the different types of investments is crucial for building wealth.'
    },
    {
      title: 'Debt Management',
      content: 'Managing debt effectively is key to financial health. Learn about different types of debt and strategies to pay them off efficiently.'
    },
    {
      title: 'Retirement Planning',
      content: 'Planning for retirement is vital to ensure you have enough funds to live comfortably. Explore different retirement accounts and savings strategies.'
    }
  ];

  return (
    <div className={styles.financialLessons}>
      <h2 className={styles.title}>Financial Lessons</h2>
      <ul className={styles.lessonList}>
        {lessons.map((lesson, index) => (
          <li key={index} className={styles.lessonItem}>
            <h3 className={styles.lessonTitle}>{lesson.title}</h3>
            <p className={styles.lessonContent}>{lesson.content}</p>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default FinancialLessons;