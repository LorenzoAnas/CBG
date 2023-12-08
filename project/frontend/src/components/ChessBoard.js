// src/components/ChessBoard.js

import React from 'react';
import styles from '../styles/ChessBoard.module.css';

const ChessBoard = () => {
  const boardSize = 8;
  const letters = 'abcdefgh'.split('');
  const numbers = Array.from({ length: boardSize }, (_, i) => boardSize - i); // Reversed for proper order
  let squares = [];

  for (let y = 0; y < boardSize; y++) {
    for (let x = 0; x < boardSize; x++) {
      const isDarkSquare = (x + y) % 2 === 1;
      squares.push(
        <div
          key={`${x}-${y}`}
          className={isDarkSquare ? styles.darkSquare : styles.lightSquare}
        />
      );
    }
  }

  return (
    <div className={styles.chessBoardWrapper}>
      <div className={styles.coordinatesVertical}>
        {numbers.map((number) => (
          <div key={number} className={styles.coordinate}>{number}</div>
        ))}
      </div>
      <div>
        <div className={styles.chessBoard}>
          {squares}
        </div>
        <div className={styles.coordinatesHorizontal}>
          {letters.map((letter) => (
            <div key={letter} className={styles.coordinate}>{letter}</div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ChessBoard;