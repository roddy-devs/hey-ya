import React, { useState, useEffect } from 'react';
import api from '../api';
import './Scoreboard.css';

function Scoreboard({ activeSession, setActiveSession }) {
  const [currentHole, setCurrentHole] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (activeSession) {
      loadActiveSession();
    }
  }, [activeSession]);

  const loadActiveSession = async () => {
    try {
      const response = await api.get(`/sessions/${activeSession.id}/`);
      setActiveSession(response.data);
      
      // Get the current active hole
      const holes = response.data.holes;
      if (holes && holes.length > 0) {
        const lastHole = holes[holes.length - 1];
        if (!lastHole.end_time) {
          setCurrentHole(lastHole);
        }
      }
    } catch (error) {
      console.error('Error loading session:', error);
    }
  };

  const startSession = async () => {
    setLoading(true);
    try {
      const response = await api.post('/sessions/', {});
      setActiveSession(response.data);
      
      // Start first hole
      await advanceHole(response.data.id);
    } catch (error) {
      console.error('Error starting session:', error);
      alert('Failed to start session');
    } finally {
      setLoading(false);
    }
  };

  const advanceHole = async (sessionId = activeSession?.id) => {
    if (!sessionId) return;
    
    setLoading(true);
    try {
      const response = await api.post(`/sessions/${sessionId}/advance_hole/`);
      setActiveSession(response.data.session);
      setCurrentHole(response.data.current_hole);
    } catch (error) {
      console.error('Error advancing hole:', error);
      alert('Failed to advance hole');
    } finally {
      setLoading(false);
    }
  };

  const recordBallDrop = async () => {
    if (!activeSession?.id) return;
    
    setLoading(true);
    try {
      const response = await api.post(`/sessions/${activeSession.id}/record_ball_drop/`);
      setActiveSession(response.data.session);
      setCurrentHole(response.data.current_hole);
    } catch (error) {
      console.error('Error recording ball drop:', error);
      alert('Failed to record ball drop');
    } finally {
      setLoading(false);
    }
  };

  const endSession = async () => {
    if (!activeSession?.id) return;
    
    if (!window.confirm('Are you sure you want to end this session?')) {
      return;
    }
    
    setLoading(true);
    try {
      await api.post(`/sessions/${activeSession.id}/end_session/`);
      setActiveSession(null);
      setCurrentHole(null);
      alert('Session ended!');
    } catch (error) {
      console.error('Error ending session:', error);
      alert('Failed to end session');
    } finally {
      setLoading(false);
    }
  };

  if (!activeSession) {
    return (
      <div className="scoreboard-container">
        <div className="start-screen">
          <h2>Ready to Play?</h2>
          <button 
            className="start-button" 
            onClick={startSession}
            disabled={loading}
          >
            {loading ? 'Starting...' : 'Start Session'}
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="scoreboard-container">
      <div className="scoreboard">
        <div className="stats-row">
          <div className="stat-box">
            <div className="stat-label">Loops</div>
            <div className="stat-value">{activeSession.total_loops}</div>
          </div>
          <div className="stat-box highlight">
            <div className="stat-label">Hole</div>
            <div className="stat-value">{currentHole?.hole_number || '-'}</div>
          </div>
        </div>

        <div className="score-display">
          <div className="score-label">Total Score</div>
          <div className="score-value">{activeSession.total_score}</div>
        </div>

        <div className="stats-row">
          <div className="stat-box">
            <div className="stat-label">Ball Drops</div>
            <div className="stat-value current">{currentHole?.ball_drops || 0}</div>
            <div className="stat-sublabel">/ {activeSession.total_ball_drops} total</div>
          </div>
        </div>

        <div className="controls">
          <button 
            className="control-button drop-button"
            onClick={recordBallDrop}
            disabled={loading || !currentHole}
          >
            ⚫ Ball Drop
          </button>
          <button 
            className="control-button advance-button"
            onClick={() => advanceHole()}
            disabled={loading || !currentHole}
          >
            ➡️ Next Hole
          </button>
          <button 
            className="control-button end-button"
            onClick={endSession}
            disabled={loading}
          >
            🏁 End Session
          </button>
        </div>
      </div>
    </div>
  );
}

export default Scoreboard;
