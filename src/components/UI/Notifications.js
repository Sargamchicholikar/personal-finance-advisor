import React from 'react';
import styles from './Notifications.module.css';

const Notifications = ({ notifications }) => {
  return (
    <div className={styles.notificationsContainer}>
      {notifications.length === 0 ? (
        <p className={styles.noNotifications}>No notifications at this time.</p>
      ) : (
        <ul className={styles.notificationsList}>
          {notifications.map((notification, index) => (
            <li key={index} className={styles.notificationItem}>
              {notification}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default Notifications;