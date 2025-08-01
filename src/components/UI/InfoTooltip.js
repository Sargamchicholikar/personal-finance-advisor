import React from 'react';
import styles from './InfoTooltip.module.css';

const InfoTooltip = ({ text }) => (
  <span
    className={styles.tooltip}
    role="tooltip"
    aria-label={text}
    title={text}
  >
    ℹ️
  </span>
);

export default InfoTooltip;