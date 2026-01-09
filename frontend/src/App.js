import React, { useState, useEffect } from 'react';
import './App.css';
import api from './api';
import Scoreboard from './components/Scoreboard';
import SessionHistory from './components/SessionHistory';
import Login from './components/Login';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [activeSession, setActiveSession] = useState(null);
  const [view, setView] = useState('scoreboard'); // 'scoreboard' or 'history'

  useEffect(() => {
    // Check if user is authenticated
    checkAuth();
  }, []);

  const checkAuth = async () => {
    try {
      const response = await api.get('/sessions/');
      setIsAuthenticated(true);
    } catch (error) {
      setIsAuthenticated(false);
    }
  };

  const handleLogin = () => {
    setIsAuthenticated(true);
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
    setActiveSession(null);
  };

  if (!isAuthenticated) {
    return <Login onLogin={handleLogin} />;
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>🍺 Ice Cold Beer</h1>
        <nav>
          <button 
            className={view === 'scoreboard' ? 'active' : ''} 
            onClick={() => setView('scoreboard')}
          >
            Play
          </button>
          <button 
            className={view === 'history' ? 'active' : ''} 
            onClick={() => setView('history')}
          >
            History
          </button>
          <button onClick={handleLogout}>Logout</button>
        </nav>
      </header>
      <main>
        {view === 'scoreboard' ? (
          <Scoreboard 
            activeSession={activeSession} 
            setActiveSession={setActiveSession} 
          />
        ) : (
          <SessionHistory />
        )}
      </main>
    </div>
  );
}

export default App;

