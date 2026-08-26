import { Link, useLocation, useNavigate } from 'react-router-dom';
import { logout as clearRemoteSession } from '../api/auth';

export default function Sidebar({ onLogout }) {
  const location = useLocation();
  const navigate = useNavigate();

  const menuItems = [
    { path: '/dashboard', label: 'Dashboard', icon: '📊' },
    { path: '/events', label: 'Events', icon: 'CAL' },
    { path: '/committees', label: 'Committees', icon: 'COM' },
    { path: '/members', label: 'Members', icon: '👥' },
    { path: '/attendance', label: 'Attendance', icon: '✅' },
    { path: '/announcements', label: 'Announcements', icon: '📢' },
    { path: '/notifications', label: 'Notifications', icon: '🔔' },
    { path: '/documents', label: 'Documents', icon: 'DOC' },
    { path: '/social', label: 'Community', icon: 'SOC' },
    { path: '/profile', label: 'My Profile', icon: 'ME' },
    { path: '/visitors', label: 'Visitors', icon: 'VIS' },
    { path: '/finances', label: 'Finances', icon: 'FIN' },
    { path: '/reports', label: 'Reports', icon: 'REP' },
  ];

  const handleLogout = async () => {
    try {
      await clearRemoteSession();
    } finally {
      if (onLogout) onLogout();
      navigate('/login');
    }
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