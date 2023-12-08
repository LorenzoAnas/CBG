import React from 'react';
import ChessGamePage from './pages/ChessGamePage'; // Import the ChessGamePage component
import './App.css'; // Keep the App-wide styles, if any

function App() {
  return (
    <div className="App">
      <ChessGamePage /> {/* Render the ChessGamePage component */}
    </div>
  );
}

export default App;