// src/components/Header.js

import React from 'react';
import styles from '../styles/Header.module.css';

const Header = () => {
  return (
    <header className={styles.header}>
      {/* Content for header like title, navigation, etc. */}
      <h1>Chess Game</h1>
    </header>
  );
};

export default Header;