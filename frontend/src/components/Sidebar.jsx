import { Link, useLocation, useNavigate } from 'react-router-dom';

const API_BASE = import.meta.env.VITE_API_BASE_URL || '';

export default function Sidebar({ onLogout }) {
  const location = useLocation();
  const navigate = useNavigate();

  const menuItems = [
    { path: '/dashboard', label: 'Dashboard', icon: '📊' },
    { path: '/events', label: 'Events', icon: '' },
    { path: '/committees', label: 'Committees', icon: '' },
    { path: '/members', label: 'Members', icon: '👥' },
    { path: '/attendance', label: 'Attendance', icon: '✅' },
    { path: '/announcements', label: 'Announcements', icon: '📢' },
  ];

  const handleLogout = async () => {
    const refresh = localStorage.getItem('cims_refresh_token');
    const token = localStorage.getItem('cims_access_token');
    if (refresh && token) {
      await fetch(`${API_BASE}/api/auth/logout/`, {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ refresh }),
      }).catch(() => {});
    }
    localStorage.removeItem('cims_access_token');
    localStorage.removeItem('cims_refresh_token');
    onLogout();
    navigate('/');
  };

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <img src="/images/church-emblem.png" alt="UNZA CIMS" className="sidebar-logo" />
        <h2>UNZA CIMS</h2>
      </div>
      <nav className="sidebar-nav">
        {menuItems.map((item) => (
          <Link
            key={item.path}
            to={item.path}
            className={`sidebar-link ${location.pathname === item.path ? 'active' : ''}`}
          >
            <span className="sidebar-icon">{item.icon}</span>
            <span className="sidebar-text">{item.label}</span>
          </Link>
        ))}
      </nav>
      <button type="button" className="sidebar-link sidebar-logout" onClick={handleLogout}>
        <span className="sidebar-icon">↪</span>
        <span className="sidebar-text">Logout</span>
      </button>
    </aside>
  );
}