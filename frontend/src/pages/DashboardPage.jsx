import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

const API_BASE = 'http://127.0.0.1:8000';

export default function DashboardPage() {
  const [userData, setUserData] = useState(null);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('cims_demo_access_token');
    if (!token) {
      navigate('/login');
      return;
    }

    fetch(`${API_BASE}/api/auth/dashboard/`, {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    .then(res => res.ok ? res.json() : Promise.reject())
    .then(data => {
      setUserData(data.user || {});
      setStats(data.statistics || {});
    })
    .catch(err => console.error("Dashboard error:", err))
    .finally(() => setLoading(false));
  }, [navigate]);

  if (loading) return <div className="loading-screen"><div className="spinner"></div></div>;

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