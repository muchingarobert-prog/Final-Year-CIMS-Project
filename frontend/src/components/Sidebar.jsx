import { Link, useLocation, useNavigate } from 'react-router-dom';
import { logout as clearRemoteSession } from '../api/auth';
import { useAuth } from '../context/AuthContext';

const managementRoles = ['SUPER_USER', 'ADMIN_USER', 'HIGH_PRIVILEGE_USER'];

export default function Sidebar({ onLogout, isOpen = false, onNavigate = () => {} }) {
  const location = useLocation();
  const navigate = useNavigate();
  const { user } = useAuth();

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
    { path: '/visitors', label: 'Visitors', icon: 'VIS', roles: managementRoles },
    { path: '/finances', label: 'Finance', icon: 'FIN', roles: managementRoles },
    { path: '/reports', label: 'Reports', icon: 'REP', roles: managementRoles },
  ];

  const visibleItems = menuItems.filter((item) => !item.roles || item.roles.includes(user?.role));

  const handleLogout = async () => {
    try {
      await clearRemoteSession();
    } finally {
      if (onLogout) onLogout();
      navigate('/login');
    }
  };

  return (
    <aside className={`sidebar ${isOpen ? 'sidebar-open' : ''}`}>
      <div className="sidebar-header">
        <img src="/images/church-emblem.png" alt="New Apostolic Church emblem" className="sidebar-logo" />
        <div className="brand-lockup"><strong>New Apostolic Church</strong><span>UNZA</span></div>
      </div>
      <nav className="sidebar-nav">
        {visibleItems.map((item) => (
          <Link
            key={item.path}
            to={item.path}
            className={`sidebar-link ${location.pathname === item.path ? 'active' : ''}`}
            onClick={onNavigate}
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