import { useEffect, useState } from 'react';
import { apiRequest } from '../api/client';
import Loading from '../components/Loading';
import ErrorMessage from '../components/ErrorMessage';

export default function DashboardPage() {
  const [userData, setUserData] = useState(null);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    apiRequest('/api/auth/dashboard/')
    .then(data => {
      setUserData(data.user || {});
      setStats(data.statistics || {});
    })
    .catch(err => setError(err.message || 'Unable to load dashboard.'))
    .finally(() => setLoading(false));
  }, []);

  if (loading) return <Loading message="Loading dashboard..." />;

  const userName = userData?.first_name || userData?.username || 'Member';

  return (
    <div className="professional-dashboard">
      {/* Church Branding Section */}
      <div className="church-branding-section">
        <div className="church-emblem-container">
          <img src="/images/church-emblem.png" alt="Church Emblem" className="main-church-emblem" />
          <h1 className="church-main-title">New Apostolic Church</h1>
          <h2 className="church-subtitle">UNZA Congregation</h2>
          <p className="church-tagline">Congregation Information Management System</p>
        </div>
      </div>

      {/* Welcome Section */}
      <div className="welcome-section">
        <h3>Welcome, {userName}!</h3>
        <p>Select a module from the sidebar to get started</p>
      </div>
      {error && <ErrorMessage message={error} />}

      {/* Quick Stats */}
      <div className="quick-stats-section">
        <div className="stat-card-blue">
          <div className="stat-icon">📅</div>
          <div className="stat-info">
            <div className="stat-number">{stats?.events || 0}</div>
            <div className="stat-label">Upcoming Events</div>
          </div>
        </div>
        <div className="stat-card-blue">
          <div className="stat-icon">👥</div>
          <div className="stat-info">
            <div className="stat-number">{stats?.committees || 0}</div>
            <div className="stat-label">My Committees</div>
          </div>
        </div>
        <div className="stat-card-blue">
          <div className="stat-icon">✅</div>
          <div className="stat-info">
            <div className="stat-number">{stats?.attendance || 0}</div>
            <div className="stat-label">Attendance</div>
          </div>
        </div>
        <div className="stat-card-blue">
          <div className="stat-icon">🔔</div>
          <div className="stat-info">
            <div className="stat-number">{stats?.unread_notifications || 0}</div>
            <div className="stat-label">Notifications</div>
          </div>
        </div>
      </div>
    </div>
  );
}