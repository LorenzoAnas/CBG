// src/components/Sidebar.js

import React from 'react';
import styles from '../styles/Sidebar.module.css';

const Sidebar = () => {
  return (
    <aside className={styles.sidebar}>
      {/* Sidebar content like game options, user profile, etc. */}
      <p>Sidebar content here.</p>
    </aside>
  );
};

export default Sidebar;