// src/components/ChessBoard.js

import React, { useState } from 'react';
import styles from '../styles/ChessBoard.module.css';

// Import the images
import bishopBlack from '../assets/blackPieces/bishopBlack.png';
import kingBlack from '../assets/blackPieces/kingBlack.png';
import knightBlack from '../assets/blackPieces/knightBlack.png';
import pawnBlack from '../assets/blackPieces/pawnBlack.png';
import queenBlack from '../assets/blackPieces/queenBlack.png';
import rookBlack from '../assets/blackPieces/rookBlack.png';
import bishopWhite from '../assets/whitePieces/bishopWhite.png';
import kingWhite from '../assets/whitePieces/kingWhite.png';
import knightWhite from '../assets/whitePieces/knightWhite.png';
import pawnWhite from '../assets/whitePieces/pawnWhite.png';
import queenWhite from '../assets/whitePieces/queenWhite.png';
import rookWhite from '../assets/whitePieces/rookWhite.png';
import moveSound from '../assets/sounds/moveSound.mp3';

const ChessBoard = () => {
  const boardSize = 8;
  const letters = 'abcdefgh'.split('');
  const numbers = Array.from({ length: boardSize }, (_, i) => boardSize - i); // Reversed for proper order

  // Create the initial state of the chessboard
  const initialBoardState = [
    [rookBlack, knightBlack, bishopBlack, queenBlack, kingBlack, bishopBlack, knightBlack, rookBlack],
    Array(8).fill(pawnBlack),
    Array(8).fill(null),
    Array(8).fill(null),
    Array(8).fill(null),
    Array(8).fill(null),
    Array(8).fill(pawnWhite),
    [rookWhite, knightWhite, bishopWhite, queenWhite, kingWhite, bishopWhite, knightWhite, rookWhite],
  ];

  const [boardState, setBoardState] = useState(initialBoardState);

  const handleDragStart = (e, position) => {
    const piece = boardState[position.y][position.x];
    e.dataTransfer.setData('piece', piece);
    e.dataTransfer.setData('position', JSON.stringify(position));
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const moveSoundEffect = new Audio(moveSound);

  const handleDrop = (e, position) => {
    e.preventDefault();

    const piece = e.dataTransfer.getData('piece');
    const oldPosition = JSON.parse(e.dataTransfer.getData('position'));

    const newBoardState = [...boardState];
    newBoardState[oldPosition.y][oldPosition.x] = null;
    newBoardState[position.y][position.x] = piece;

    setBoardState(newBoardState);

    // Play the sound
    moveSoundEffect.play();
  };

  let squares = [];

  for (let y = 0; y < boardSize; y++) {
    for (let x = 0; x < boardSize; x++) {
      const isDarkSquare = (x + y) % 2 === 1;
      squares.push(
        <div
          key={`${x}-${y}`}
          className={isDarkSquare ? styles.darkSquare : styles.lightSquare}
          onDragOver={handleDragOver}
          onDrop={(e) => handleDrop(e, { x, y })}
        >
          {boardState[y][x] && (
            <img
              src={boardState[y][x]}
              alt=""
              draggable
              onDragStart={(e) => handleDragStart(e, { x, y })}
            />
          )}
        </div>
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