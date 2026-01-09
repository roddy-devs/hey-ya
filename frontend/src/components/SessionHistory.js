import React, { useState, useEffect } from 'react';
import api from '../api';
import './SessionHistory.css';

function SessionHistory() {
  const [sessions, setSessions] = useState([]);
  const [selectedSession, setSelectedSession] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadSessions();
  }, []);

  const loadSessions = async () => {
    setLoading(true);
    try {
      const response = await api.get('/sessions/');
      setSessions(response.data.results || response.data);
    } catch (error) {
      console.error('Error loading sessions:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadSessionDetail = async (sessionId) => {
    try {
      const response = await api.get(`/sessions/${sessionId}/`);
      setSelectedSession(response.data);
    } catch (error) {
      console.error('Error loading session detail:', error);
    }
  };

  const formatDuration = (duration) => {
    if (!duration) return 'N/A';
    
    // Duration is in format like "0:15:30" (hours:minutes:seconds)
    const parts = duration.split(':');
    if (parts.length === 3) {
      const hours = parseInt(parts[0]);
      const minutes = parseInt(parts[1]);
      const seconds = Math.floor(parseFloat(parts[2]));
      
      if (hours > 0) {
        return `${hours}h ${minutes}m`;
      }
      return `${minutes}m ${seconds}s`;
    }
    return duration;
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  if (loading) {
    return <div className="loading">Loading sessions...</div>;
  }

  if (selectedSession) {
    return (
      <div className="session-detail">
        <button className="back-button" onClick={() => setSelectedSession(null)}>
          ← Back to History
        </button>
        
        <div className="detail-header">
          <h2>Session Details</h2>
          <div className="detail-stats">
            <div className="detail-stat">
              <span className="label">Date:</span>
              <span className="value">{formatDate(selectedSession.start_time)}</span>
            </div>
            <div className="detail-stat">
              <span className="label">Duration:</span>
              <span className="value">{formatDuration(selectedSession.duration)}</span>
            </div>
            <div className="detail-stat">
              <span className="label">Score:</span>
              <span className="value">{selectedSession.total_score}</span>
            </div>
            <div className="detail-stat">
              <span className="label">Loops:</span>
              <span className="value">{selectedSession.total_loops}</span>
            </div>
            <div className="detail-stat">
              <span className="label">Ball Drops:</span>
              <span className="value">{selectedSession.total_ball_drops}</span>
            </div>
          </div>
        </div>

        <div className="holes-list">
          <h3>Holes ({selectedSession.holes?.length || 0})</h3>
          <table className="holes-table">
            <thead>
              <tr>
                <th>Loop</th>
                <th>Hole</th>
                <th>Score</th>
                <th>Time</th>
                <th>Drops</th>
              </tr>
            </thead>
            <tbody>
              {selectedSession.holes?.map((hole) => (
                <tr key={hole.id}>
                  <td>{hole.loop_index}</td>
                  <td>{hole.hole_number}</td>
                  <td>{hole.final_score}</td>
                  <td>{hole.completion_time ? `${hole.completion_time.toFixed(1)}s` : 'N/A'}</td>
                  <td>{hole.ball_drops}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    );
  }

  return (
    <div className="session-history">
      <h2>Session History</h2>
      
      {sessions.length === 0 ? (
        <div className="no-sessions">
          <p>No sessions yet. Start playing to create your first session!</p>
        </div>
      ) : (
        <div className="sessions-list">
          {sessions.map((session) => (
            <div 
              key={session.id} 
              className="session-card"
              onClick={() => loadSessionDetail(session.id)}
            >
              <div className="session-date">
                {formatDate(session.start_time)}
              </div>
              <div className="session-stats">
                <div className="session-stat">
                  <span className="stat-label">Score</span>
                  <span className="stat-value">{session.total_score}</span>
                </div>
                <div className="session-stat">
                  <span className="stat-label">Loops</span>
                  <span className="stat-value">{session.total_loops}</span>
                </div>
                <div className="session-stat">
                  <span className="stat-label">Drops</span>
                  <span className="stat-value">{session.total_ball_drops}</span>
                </div>
                <div className="session-stat">
                  <span className="stat-label">Duration</span>
                  <span className="stat-value">{formatDuration(session.duration)}</span>
                </div>
              </div>
              {session.is_active && (
                <div className="active-badge">Active</div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default SessionHistory;
