// src/pages/ChessGamePage.js

import React from 'react';
import Header from '../components/Header';
import Sidebar from '../components/Sidebar';
import ChessBoard from '../components/ChessBoard';
import styles from '../styles/ChessGamePage.module.css';

const ChessGamePage = () => {
  return (
    <div className={styles.chessGamePage}>
      <div className={styles.mainContent}>
        <ChessBoard />
      </div>
    </div>
  );
};

export default ChessGamePage;
